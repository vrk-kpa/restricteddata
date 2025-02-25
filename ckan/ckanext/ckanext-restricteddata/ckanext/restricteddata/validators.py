import json
import logging

from ckanext.scheming.validation import scheming_validator
from ckan.plugins import toolkit
from . import plugin
from ckan import model
from ckan.logic import validators

_ = toolkit._
log = logging.getLogger(__name__)


def repeating_text(key, data, errors, context):
    """
    Accept repeating text input in the following forms
    and convert to a json list for storage:

    1. a list of strings, eg.

       ["Person One", "Person Two"]

    2. a single string value to allow single text fields to be
       migrated to repeating text

       "Person One"

    3. separate fields per language (for form submissions):

       fieldname-0 = "Person One"
       fieldname-1 = "Person Two"
    """
    # just in case there was an error before our validator,
    # bail out here because our errors won't be useful
    if errors[key]:
        return

    value = data[key]
    # 1. list of strings or 2. single string
    if value is not toolkit.missing:
        if isinstance(value, str):
            value = [value]
        if not isinstance(value, list):
            errors[key].append(_('expecting list of strings'))
            return

        out = []
        for element in value:
            if isinstance(element, bytes):
                try:
                    element = element.decode('utf-8')
                except UnicodeDecodeError:
                    errors[key]. append(_('invalid encoding for "%s" value')
                                        % toolkit.lang)
                    continue
            elif not isinstance(element, str):
                errors[key].append(_('invalid type for repeating text: %r')
                                   % element)
                continue
            out.append(element)

        if not errors[key]:
            data[key] = json.dumps(out)
        return

    # 3. separate fields
    found = {}
    prefix = key[-1] + '-'
    extras = data.get(key[:-1] + ('__extras',), {})

    for name, text in extras.items():
        if not name.startswith(prefix):
            continue
        if not text:
            continue
        index = name.split('-', 1)[1]
        try:
            index = int(index)
        except ValueError:
            continue
        found[index] = text

    out = [found[i] for i in sorted(found)]
    data[key] = json.dumps(out)


def repeating_text_output(value):
    """
    Return stored json representation as a list, if
    value is already a list just pass it through.
    """
    if isinstance(value, list):
        return value
    if value is None:
        return []
    try:
        return json.loads(value)
    except ValueError:
        return [value]


def repeating_email(key, data, errors, context):
    if errors[key]:
        return

    value_json = data[key]
    value = json.loads(value_json)

    if not isinstance(value, list):
        errors[key].append(_('expecting a list'))
        return

    email_validator = toolkit.get_validator('email_validator')
    for item in value:
        email_validator(item, context)


@scheming_validator
def required_languages(field, schema):
    languages = field.get('required_languages', [])

    def validator(key, data, errors, context):
        if errors[key]:
            return

        value = data[key]

        if value is not toolkit.missing:
            if isinstance(value, str):
                try:
                    value = json.loads(value)
                except ValueError:
                    errors[key].append(_('Failed to decode JSON string'))
                    return
                except UnicodeDecodeError:
                    errors[key].append(_('Invalid encoding for JSON string'))
                    return
            if not isinstance(value, dict):
                errors[key].append(_('expecting JSON object'))
                return

            for lang in languages:
                if value.get(lang, '') == '':
                    error = _('Required language "%s" missing') % lang
                    errors[key].append(error)
            return

        prefix = key[-1] + '-'
        extras = data.get(key[:-1] + ('__extras',), {})

        for lang in languages:
            if extras.get(prefix + lang, '') == '':
                errors[key].append(_('Required language "%s" missing') % lang)

    return validator


def override_field_with_default_translation(overridden_field_name):
    @scheming_validator
    def implementation(field, schema):

        from ckan.lib.navl.dictization_functions import missing

        default_lang = toolkit.config.get('ckan.locale_default', 'en')

        def validator(key, data, errors, context):
            value = data[key]
            override_value = missing

            if value is not missing:
                if isinstance(value, str):
                    try:
                        value = json.loads(value)
                    except ValueError:
                        errors[key].append(_('Failed to decode JSON string'))
                        return
                    except UnicodeDecodeError:
                        errors[key].append(_('Invalid encoding for JSON string'))
                        return
                if not isinstance(value, dict):
                    errors[key].append(_('expecting JSON object'))
                    return

                override_value = value.get(default_lang, missing)

            if override_value not in (None, missing):
                overridden_key = tuple(overridden_field_name.split('.'))
                data[overridden_key] = override_value

        return validator

    return implementation


def populate_required_languages_from_field_if_missing(field_name):
    @scheming_validator
    def validator(field, schema):
        def inner(key, data, errors, context):
            languages = field.get('required_languages', [])
            value = {} if data[key] is toolkit.missing else data[key]
            # Assumption: subject field is a sibling to the object field
            default_value = data[key[:-1] + (field_name,)]

            if isinstance(value, str):
                try:
                    value = json.loads(value)
                except ValueError:
                    errors[key].append(_('Failed to decode JSON string'))
                    return
                except UnicodeDecodeError:
                    errors[key].append(_('Invalid encoding for JSON string'))
                    return

            if not isinstance(value, dict):
                errors[key].append(_('expecting JSON object'))
                return

            for lang in languages:
                if value.get(lang, '') == '':
                    value[lang] = default_value

            data[key] = json.dumps(value)

        return inner

    return validator


def create_fluent_tags(vocab):
    def callable(key, data, errors, context):
        value = data[key]
        if isinstance(value, str):
            value = json.loads(value)
        if isinstance(value, dict):
            for lang in value:
                add_to_vocab(context, value[lang], vocab + '_' + lang)
            data[key] = json.dumps(value)

    return callable


def add_to_vocab(context, tags, vocab):

    defer = context.get('defer', False)
    try:
        v = toolkit.get_action('vocabulary_show')(context, {'id': vocab})
    except toolkit.ObjectNotFound:
        v = plugin.create_vocabulary(vocab, defer)

    assert v is not None
    context['vocabulary'] = model.Vocabulary.get(v.get('id'))
    if isinstance(tags, str):
        tags = [tags]

    for tag in tags:
        validators.tag_length_validator(tag, context)
        validators.tag_name_validator(tag, context)

        try:
            validators.tag_in_vocabulary_validator(tag, context)
        except toolkit.Invalid:
            plugin.create_tag_to_vocabulary(tag, vocab, defer)


@scheming_validator
def keep_old_value_if_missing(field, schema):
    from ckan.lib.navl.dictization_functions import missing, flatten_dict
    from ckan.logic import get_action

    def validator(key, data, errors, context):

        if 'package' not in context and 'group' not in context:
            return

        action = ''
        context_var = ''
        if 'package' in context:
            action = 'package'
            context_var = 'package'

        if 'group' in context:
            action = 'organization'
            context_var = 'group'

        data_dict = flatten_dict(get_action(action + '_show')(context, {'id': context[context_var].id}))

        if key not in data or data[key] is missing:
            if key in data_dict:
                data[key] = data_dict[key]

    return validator


def repeating_url(key, data, errors, context):
    if errors[key]:
        return

    value_json = data[key]
    value = json.loads(value_json)

    if not isinstance(value, list):
        errors[key].append(_('expecting a list'))
        return

    url_validator = toolkit.get_validator('url_validator')
    for item in value:
        url_validator(key, {key: item}, errors, context)


def convert_to_json_compatible_str_if_str(value):
    if isinstance(value, str):
        if value == "":
            return json.dumps({})
        try:
            json.loads(value)
        except ValueError:
            value = json.dumps({'fi': value})
        return value


def highvalue_category(key, data, errors, context):
    highvalue = data.get(("highvalue",), False)
    if highvalue is True:
        value = data.get(key)
        if not value:
            errors[key].append(_('You must select at least 1 high value category'))

        return data[key]


def highvalue(key, data, errors, context):
    value = data[key]

    # Remove highvalue categories if highvalue is false
    if value is False:
        removed_keys = []
        for k in data.keys():
            if 'highvalue_category' in k:
                removed_keys.append(k)

        for k in removed_keys:
            data[k] = []
