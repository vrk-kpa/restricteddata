from ckan import model
from ckan.common import c
from ckan.plugins import toolkit
from ckan.lib import i18n
from ckanext.scheming.helpers import lang
from ckan.logic import NotFound
from flask import has_request_context
from logging import getLogger
from html import escape as html_escape
from urllib.parse import quote

from ckan.lib.helpers import build_nav_main as ckan_build_nav_main


log = getLogger(__name__)
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
    return t


def get_lang_prefix():
    language = i18n.get_lang()
    if language in _LOCALE_ALIASES:
        language = _LOCALE_ALIASES[language]

    return language


def call_toolkit_function(fn, args, kwargs):
    return getattr(toolkit, fn)(*args, **kwargs)


def get_homepage_groups():
    return toolkit.get_action('group_list')({}, {
        'all_fields': True,
        'include_dataset_count': True,
        'include_extras': True,
    })


def scheming_category_list(args):
    # FIXME: sometimes this might return 0 categories if in development

    try:
        context = {'model': model, 'session': model.Session, 'ignore_auth': True}
        group_ids = toolkit.get_action('group_list')(context, {})
    except NotFound:
        return None
    else:
        category_list = []

        # filter groups to those user is allowed to edit
        group_authz = toolkit.get_action('group_list_authz')({
            'model': model, 'session': model.Session, 'user': c.user
        }, {})

        user_group_ids = set(group['name'] for group in group_authz)
        group_ids = [group for group in group_ids if group in user_group_ids]

        for group in group_ids:
            try:
                context = {'model': model, 'session': model.Session, 'ignore_auth': True}
                group_details = toolkit.get_action('group_show')(context, {'id': group, 'include_users': False,
                                                                   'include_dataset_count': False,
                                                                   'include_groups': False,
                                                                   'include_tags': False,
                                                                   'include_followers': False})
            except Exception as e:
                log.error(e)
                return None

            category_list.append({
                "value": group,
                "label": group_details.get('title_translated')
            })

    return category_list


# Copied from ckanext-pages to add multilingual title support
def pages_build_nav_main(*args):
    about_menu = toolkit.asbool(toolkit.config.get('ckanext.pages.about_menu', True))
    group_menu = toolkit.asbool(toolkit.config.get('ckanext.pages.group_menu', True))
    org_menu = toolkit.asbool(toolkit.config.get('ckanext.pages.organization_menu', True))

    new_args = []
    for arg in args:
        if arg[0] in 'home.about' and not about_menu:
            continue
        if arg[0] in 'home.group_index' and not org_menu:
            continue
        if arg[0] in 'home.organizations_index' and not group_menu:
            continue
        new_args.append(arg)

    output = ckan_build_nav_main(*new_args)

    # do not display any private pages in menu even for sysadmins
    pages_list = toolkit.get_action('ckanext_pages_list')(None, {'order': True, 'private': False})

    page_name = ''
    is_current_page = toolkit.get_endpoint() in (('pages', 'show'), ('pages', 'blog_show'))

    if is_current_page:
        page_name = toolkit.request.path.split('/')[-1]

    language = get_lang_prefix()

    for page in pages_list:
        type_ = 'blog' if page['page_type'] == 'blog' else 'pages'
        name = quote(page['name'])
        if page.get('title_' + language):
            title = html_escape(page['title' + '_' + language])
        else:
            title = html_escape(page['title'])
        link = toolkit.h.literal(u'<a href="/{}/{}">{}</a>'.format(type_, name, title))
        if page['name'] == page_name:
            li = toolkit.literal('<li class="active">') + link + toolkit.literal('</li>')
        else:
            li = toolkit.literal('<li>') + link + toolkit.literal('</li>')
        output = output + li

    return output

@toolkit.chained_helper
def build_nav_main(next, *args, pages=False):
    if pages:
        return pages_build_nav_main(*args)
    else:
        return ckan_build_nav_main(*args)


def get_translated_logo(language: str):
    site_logo = toolkit.config.get('ckan.site_logo')
    if not site_logo:
        return site_logo
    else:
        [path, extension] = site_logo.rsplit('.', 1)
        return f'{path}_{language}.{extension}'


def get_assignable_groups_for_package(pkg_dict):
    context = {'model': model, 'session': model.Session, 'user': c.user}

    try:
        toolkit.check_access('package_update', context, {'id': pkg_dict['id']})
    except toolkit.NotAuthorized:
        return []

    groups = scheming_category_list(None)
    package_group_ids = set(g['name'] for g in pkg_dict.get('groups', []))

    return [{'name': g['value'], 'title_translated': g['label']}
            for g in groups
            if g['value'] not in package_group_ids]


highvalue_categories = {
    "meteorological": "Meteorological",
    "companies-and-company-ownership": "Companies and company ownership",
    "geospatial": "Geospatial",
    "mobility": "Mobility",
    "earth-observation-and-environment": "Earth observation and environment",
    "statistics": "Statistics"
}

def scheming_highvalue_category_list(field):
    return [{"value": category, "label": label } for category, label in highvalue_categories.items()]

def get_highvalue_category_label(value):
    return highvalue_categories.get(value, "")

def get_group_title_translations():
    context = {'model': model, 'session': model.Session}
    if has_request_context() and toolkit.g.get('user'):
        context['user'] = toolkit.g.user

    data_dict = {'all_fields': True, 'include_extras': True, 'include_dataset_count': False}
    groups = toolkit.get_action('group_list')(context, data_dict)
    return {g['name']: g.get('title_translated', {}) for g in groups}

def get_translated_groups(groups):
    context = {'model': model, 'session': model.Session}
    if has_request_context() and toolkit.g.get('user'):
        context['user'] = toolkit.g.user

    data_dict = {'groups': [g['name'] for g in groups],
                 'all_fields': True,
                 'include_extras': True,
                 'include_dataset_count': False}
    return toolkit.get_action('group_list')(context, data_dict)
