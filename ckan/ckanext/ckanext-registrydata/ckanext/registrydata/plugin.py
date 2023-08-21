import logging
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.logic import NotFound
from ckanext.pages.interfaces import IPagesSchema
from ckan.lib.plugins import DefaultTranslation

from . import helpers, validators

log = logging.getLogger(__name__)


class RegistrydataPlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IValidators)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, "templates")
        toolkit.add_public_directory(config_, "public")
        toolkit.add_resource("assets", "registrydata")

    # ITemplateHelpers

    def get_helpers(self):
        return {
            'scheming_field_only_default_required':
            helpers.scheming_field_only_default_required,
            'add_locale_to_source': helpers.add_locale_to_source,
            'is_boolean_selected': helpers.is_boolean_selected,
            'scheming_language_text_or_empty':
            helpers.scheming_language_text_or_empty,
            'get_lang_prefix': helpers.get_lang_prefix,
            'call_toolkit_function': helpers.call_toolkit_function,
        }

    # IValidators:

    def get_validators(self):
        return {
            'repeating_text': validators.repeating_text,
            'repeating_email': validators.repeating_email,
            'repeating_text_output': validators.repeating_text_output,
            'override_field_with_default_translation':
            validators.override_field_with_default_translation,
            'create_fluent_tags': validators.create_fluent_tags,
            'keep_old_value_if_missing': validators.keep_old_value_if_missing,
            'repeating_url': validators.repeating_url,
            'convert_to_json_compatible_str_if_str':
            validators.convert_to_json_compatible_str_if_str,
            'required_languages': validators.required_languages,
        }


class RegistrydataPagesPlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(IPagesSchema)

    def update_config(self, config_):
        toolkit.add_template_directory(config_, "templates_pages")

    # IPagesSchema
    def update_pages_schema(self, schema):
        schema.update({
            'title_fi': [],
            'title_sv': [],
            'title_en': [],
            'content_fi': [],
            'content_sv': [],
            'content_en': [],
            # 'submenu_order': []
            })
        return schema


def create_vocabulary(name, defer=False):
    user = toolkit.get_action('get_site_user')({'ignore_auth': True}, {})
    context = {'user': user['name']}

    try:
        data = {'id': name}
        return toolkit.get_action('vocabulary_show')(context, data)
    except NotFound:
        pass

    log.info("Creating vocab '" + name + "'")
    data = {'name': name}
    try:
        if defer:
            context['defer_commit'] = True
        return toolkit.get_action('vocabulary_create')(context, data)
    except Exception as e:
        log.error('%s' % e)


def create_tag_to_vocabulary(tag, vocab, defer=False):
    user = toolkit.get_action('get_site_user')({'ignore_auth': True}, {})
    context = {'user': user['name']}

    data = {'id': vocab}
    v = toolkit.get_action('vocabulary_show')(context, data)

    data = {
        "name": tag,
        "vocabulary_id": v['id']}

    if defer:
        context['defer_commit'] = True
    try:
        toolkit.get_action('tag_create')(context, data)
    except toolkit.ValidationError:
        pass
