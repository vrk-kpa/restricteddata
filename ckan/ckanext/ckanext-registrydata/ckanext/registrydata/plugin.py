from typing import List, Dict, Any

import logging
import json
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.logic import NotFound
from ckanext.pages.interfaces import IPagesSchema
from ckan.lib.plugins import DefaultTranslation
from flask import has_request_context
from ckanext.registrydata.cli import cli
from collections import OrderedDict

from . import helpers, validators

log = logging.getLogger(__name__)
ResourceDict = Dict[str, Any]
PackageDict = Dict[str, Any]


class RegistrydataPlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IValidators)
    plugins.implements(plugins.IPackageController, inherit=True)
    plugins.implements(plugins.IClick)
    plugins.implements(plugins.IFacets, inherit=True)

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
            'get_homepage_news': helpers.get_homepage_news,
            'get_homepage_groups': helpers.get_homepage_groups,
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

    # IPackageController

    def after_dataset_search(self, search_results, search_params) -> PackageDict:
        # Only filter results if processing a request
        if not has_request_context():
            return search_results

        if toolkit.current_user.is_authenticated and toolkit.current_user.sysadmin:
            return search_results

        results = [result for result in search_results.get('results', [])]

        for result in results:
            user_name = toolkit.g.user
            org_id = result.get('organization')
            resources = result.get('resources', [])
            allowed_resources = filter_allowed_resources(resources, org_id, user_name)
            result['resources'] = allowed_resources
            result['num_resources'] = len(allowed_resources)

        search_results['results'] = results
        return search_results

    def after_dataset_show(self, context, data_dict: PackageDict) -> PackageDict:
        # Only filter results if processing a request
        if not has_request_context():
            return data_dict

        # Skip access check if sysadmin or auth is ignored
        if context.get('ignore_auth') or (toolkit.current_user.is_authenticated
                                          and toolkit.current_user.sysadmin):
            return data_dict

        user_name = context.get('user')

        org_id = data_dict['owner_org']
        resources = data_dict.get('resources', [])
        allowed_resources = filter_allowed_resources(resources, org_id, user_name)

        data_dict['resources'] = allowed_resources
        data_dict['num_resources'] = len(allowed_resources)

        return data_dict

    def before_dataset_index(self, pkg_dict):
        # Map keywords to vocab_keywords_{lang}
        translated_vocabs = ['keywords']
        languages = ['fi', 'sv', 'en']
        for prop_key in translated_vocabs:
            prop_json = pkg_dict.get(prop_key)
            # Add only if not already there
            if not prop_json:
                continue
            prop_value = json.loads(prop_json)
            # Add for each language
            for language in languages:
                if prop_value.get(language):
                    pkg_dict['vocab_%s_%s' % (prop_key, language)] = [tag.lower() for tag in prop_value[language]]

        return pkg_dict

    # IClick

    def get_commands(self):
        return cli.get_commands()

    # IFacets

    def dataset_facets(self, facets_dict, package_type):
        lang = helpers.get_lang_prefix()
        facets_dict = OrderedDict([
            ('groups', toolkit._('Datasets')),
            ('vocab_keywords_' + lang, toolkit._('Tags')),
            ('res_format', toolkit._('Format')),
            ('license_id', toolkit._('License'))
        ])
        return facets_dict


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


def filter_allowed_resources(resources: List[ResourceDict],
                             organization_id: str, user_name: str) -> List[ResourceDict]:
    if user_name:
        user_orgs_result = toolkit.get_action('organization_list_for_user')(
            {'ignore_auth': True},
            {'id': user_name, 'permission': 'read'})
        user_orgs = [{'name': o['name'], 'id': o['id']} for o in user_orgs_result]
    else:
        user_orgs = []

    user_in_organization = any(o.get('id', None) == organization_id for o in user_orgs)

    def is_private(resource: ResourceDict) -> bool:
        return resource.get('private', False) is True

    def is_allowed(resource):
        return user_in_organization or not is_private(resource)

    return [resource for resource in resources
            if is_allowed(resource)]
