from ckan.plugins import toolkit
from ckan.lib import i18n
from ckanext.scheming.helpers import lang

_ = toolkit._

_LOCALE_ALIASES = {'en_GB': 'en'}


def scheming_field_only_default_required(field, lang):
    return bool(field
                and field.get('only_default_lang_required')
                and lang == toolkit.config.get('ckan.locale_default', 'en'))


def add_locale_to_source(kwargs, locale):
    copy = kwargs.copy()
    source = copy.get('data-module-source', None)
    if source:
        copy.update({'data-module-source': source + '_' + locale})
        return copy
    return copy


def is_boolean_selected(value, selected):
    try:
        return toolkit.asbool(value) is toolkit.asbool(selected)
    except ValueError:
        return


def scheming_language_text_or_empty(text, prefer_lang=None):
    """
    :param text: {lang: text} dict or text string
    :param prefer_lang: choose this language version if available
    Convert "language-text" to users' language by looking up
    language in dict or using gettext if not a dict
    """
    if not text:
        return ''

    if hasattr(text, 'get'):
        try:
            if prefer_lang is None:
                prefer_lang = lang()
        except TypeError:
            pass  # lang() call will fail when no user language available
        else:
            if prefer_lang in _LOCALE_ALIASES:
                prefer_lang = _LOCALE_ALIASES[prefer_lang]
            try:
                return text[prefer_lang]
            except KeyError:
                return ''

    t = _(text)
    if isinstance(t, str):
        return t.decode('utf-8')
    return t


def get_lang_prefix():
    language = i18n.get_lang()
    if language in _LOCALE_ALIASES:
        language = _LOCALE_ALIASES[language]

    return language


def call_toolkit_function(fn, args, kwargs):
    return getattr(toolkit, fn)(*args, **kwargs)


def get_site_name():
    return toolkit.config.get('ckanext.registrydata.site_name')
