from typing import List, Dict, Any

import logging
import json
import datetime
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.logic import NotFound
from ckanext.pages.interfaces import IPagesSchema
from ckan.lib.plugins import DefaultTranslation
from ckan.lib.munge import munge_title_to_name
import ckan.model as model
from flask import has_request_context
from ckanext.restricteddata.cli import cli
from collections import OrderedDict
import jwt
from flask_login import login_user, logout_user

from . import helpers, validators, views
from .logic import action, auth
import random
import base64

log = logging.getLogger(__name__)
ResourceDict = Dict[str, Any]
PackageDict = Dict[str, Any]


class RestrictedDataPlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IValidators)
    plugins.implements(plugins.IPackageController, inherit=True)
    plugins.implements(plugins.IClick)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.IFacets, inherit=True)
    plugins.implements(plugins.IActions, inherit=True)
    plugins.implements(plugins.IAuthFunctions)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, "templates")
        toolkit.add_template_directory(config_, "doc")
        toolkit.add_public_directory(config_, "public")
        toolkit.add_resource("assets", "restricteddata")

    def update_config_schema(self, schema):
        ignore_missing = toolkit.get_validator('ignore_missing')
        unicode_safe = toolkit.get_validator('unicode_safe')

        schema.update({
            f'ckanext.restricteddata.{field}_{lang}': [ignore_missing, unicode_safe]
            for field in ['info_message', 'service_alert']
            for lang in ['fi', 'sv', 'en']})

        return schema

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
            'scheming_category_list': helpers.scheming_category_list,
            'build_nav_main': helpers.build_nav_main,
            'get_translated_logo': helpers.get_translated_logo,
            'get_assignable_groups_for_package': helpers.get_assignable_groups_for_package,
            'scheming_highvalue_category_list': helpers.scheming_highvalue_category_list,
            'get_highvalue_category_label': helpers.get_highvalue_category_label,
            'get_group_title_translations': helpers.get_group_title_translations,
            'get_translated_groups': helpers.get_translated_groups
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
            'highvalue_category': validators.highvalue_category,
            'highvalue': validators.highvalue
        }

    # IPackageController

    def after_dataset_search(self, search_results, search_params) -> PackageDict:

        # Modify facet display name to be human-readable
        group_titles = helpers.get_group_title_translations()
        lang = helpers.get_lang_prefix() if has_request_context() else toolkit.config.get('ckan_locale_default', 'en')
        # TODO: handle translations for highvalue categories
        if search_results.get('search_facets'):
            for facet in search_results['search_facets']:
                if facet == "vocab_highvalue_category":
                    for facet_item in search_results['search_facets'][facet]['items']:
                        facet_item['display_name'] = helpers.get_highvalue_category_label(facet_item['name'])
                elif facet == "groups":
                    for facet_item in search_results['search_facets'][facet]['items']:
                        facet_item['display_name'] = (group_titles.get(facet_item['name'], {})
                                                      .get(lang, facet_item['display_name']))


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

        if pkg_dict.get('highvalue_category'):
            pkg_dict['vocab_highvalue_category'] = json.loads(pkg_dict.get('highvalue_category'))

        return pkg_dict

    # IClick

    def get_commands(self):
        return cli.get_commands()

    # IFacets

    def dataset_facets(self, facets_dict, package_type):
        lang = helpers.get_lang_prefix()
        facets_dict = OrderedDict([
            ('groups', toolkit._('Groups')),
            ('vocab_keywords_' + lang, toolkit._('Tags')),
            ('res_format', toolkit._('Format')),
            ('vocab_highvalue_category', toolkit._('High-value dataset category'))
        ])
        return facets_dict

    # IBlueprint

    def get_blueprint(self):
        return views.get_blueprints()

    # IActions

    def get_actions(self):
        return {
            'user_create': action.user_create,
            'member_roles_list': action.member_roles_list,
            'user_autocomplete': action.user_autocomplete
        }

    # IAuthFunctions

    def get_auth_functions(self):
        return {
            'member_create': auth.member_create,
            'member_delete': auth.member_delete,
            'api_token_create': auth.sysadmin_only,
            'user_list': auth.sysadmin_only
        }


class RestrictedDataPagesPlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(IPagesSchema)
    plugins.implements(plugins.ITemplateHelpers)

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
            'submenu_order': []
            })
        return schema

    # ITemplateHelpers
    def get_helpers(self):
        return {
            'get_submenu_content': get_submenu_content
        }


def get_submenu_content():
    pages_list = toolkit.get_action('ckanext_pages_list')(None, {'private': False})
    submenu_pages = [page for page in pages_list if page.get('submenu_order')]
    return sorted(submenu_pages, key=lambda p: p['submenu_order'])


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


class RestrictedDataPahaAuthenticationPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IAuthenticator, inherit=True)
    plugins.implements(plugins.interfaces.IActions)

    def decode_paha_jwt_token(self, key, algorithm):
        '''Tries to decode a PAHA JWT token payload from request'''

        if not (key and algorithm):
            return

        authorization = toolkit.request.headers.get('Authorization')
        if not authorization:
            return
        try:
            schema, encoded_token = authorization.split(' ', 1)
        except ValueError:
            return

        if schema != 'Bearer':
            return

        try:
            token = jwt.decode(encoded_token, key, algorithms=[algorithm])
        except Exception:
            # Fallback to regular auth if anything at all goes wrong with the token
            return

        if token.get('iss') != 'PAHA':
            return

        return token

    def create_or_authenticate_paha_user(self, token):
        '''Identifies a user based on a PAHA JWT token creating a new user if needed'''
        user_id = token['id']
        user = model.User.get(user_id)

        # Create a new user if one does not exist
        if not user:
            logout_user()
            user_email = token['email']
            user_first_name = token['firstName']
            user_last_name = token['lastName']
            user_name = f'{user_first_name}_{user_last_name}'
            if not model.User.check_name_available(user_name):
                for i in range(1, 100):
                    user_name = f'{user_first_name}_{user_last_name}_{i}'
                    if model.User.check_name_available(user_name):
                        break
                else:
                    raise RuntimeError("Could not generate an available username!")

            user_dict = {
                'id': user_id,
                'name': user_name,
                'email': user_email,
                'password': base64.a85encode(random.randbytes(128)).decode('utf-8'),
                'fullname': f'{user_first_name} {user_last_name}'
            }

            site_user_info = toolkit.get_action('get_site_user')({'ignore_auth': True}, {})
            context = {'user': site_user_info['name']}

            toolkit.get_action('user_create')(context, user_dict)

            user = model.User.get(user_id)

        if user:
            toolkit.g.user = user.name
            toolkit.g.userobj = user
            login_user(user)
            return user
        else:
            raise RuntimeError("Could not find or create PAHA user!")

    def create_or_get_paha_organization(self, token):
        log.info("create_or_get_paha_organization")
        '''Retrieves an organization based on a PAHA JWT token creating a new one if needed'''
        site_user_info = toolkit.get_action('get_site_user')({'ignore_auth': True}, {})
        organization_id = token['activeOrganizationId']
        try:
            context = {'ignore_auth': True}
            return toolkit.get_action('organization_show')(context, {'id': organization_id})

        except toolkit.ObjectNotFound:
            log.info("creating new organization")
            name_languages = ['fi', 'sv', 'en']
            organization_titles = {lang: token[f'activeOrganizationName{lang.capitalize()}']
                                   for lang in name_languages}
            organization_title = next((organization_titles[lang]
                                      for lang in name_languages
                                      if organization_titles.get(lang)), None)
            if not organization_title:
                raise RuntimeError("Could not determine a non-empty name for PAHA organization!")

            organization_name = munge_title_to_name(organization_title)

            organization_dict = {
                'id': organization_id,
                'name': organization_name,
                'title_translated': organization_titles,
                'image_url': ''
            }

            site_user_info = toolkit.get_action('get_site_user')({'ignore_auth': True}, {})
            context = {'ignore_auth': site_user_info['name']}

            organization = toolkit.get_action('organization_create')(context, organization_dict)
            from pprint import pformat
            log.info("Created organization %s", pformat(organization))
            return organization

    def temporarily_authorize_user_for_organization(self, user, organization, expires):
        '''Temporarily authorizes a user to act on behalf of an organization'''
        context = {'ignore_auth': True}
        data_dict = {
            'user': user.id,
            'organization': organization['id'],
            'expires': expires
        }
        toolkit.get_action('grant_temporary_membership')(context, data_dict)

    def identify(self):
        key = toolkit.config.get('ckanext.restricteddata.paha_jwt_key')
        algorithm = toolkit.config.get('ckanext.restricteddata.paha_jwt_algorithm')
        paha_jwt_token = self.decode_paha_jwt_token(key, algorithm)
        if paha_jwt_token:
            user = self.create_or_authenticate_paha_user(paha_jwt_token)
            organization = self.create_or_get_paha_organization(paha_jwt_token)
            # expiresIn is a timestamp expressed in milliseconds
            expires = datetime.datetime.fromtimestamp(paha_jwt_token['expiresIn'] / 1000)
            self.temporarily_authorize_user_for_organization(user, organization, expires)

        return super().identify()

    def get_actions(self):
        return {
            'grant_temporary_membership': action.grant_temporary_membership,
            'purge_expired_temporary_memberships': action.purge_expired_temporary_memberships
        }


# NOTE: DO NOT ENABLE THIS PLUGIN IN NON-LOCAL ENVIRONMENTS
class RestrictedDataResetPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.interfaces.IActions)

    def get_actions(self):
        return {
            "reset": _reset
        }

@toolkit.side_effect_free
def _reset(context, data_dict):
    # clean database
    from ckan import model
    model.repo.delete_all()

    # clear search index
    from ckan.lib.search import clear_all
    clear_all()

    # Create default sysadmin
    context = {'ignore_auth': True}
    admin_username = data_dict.get('admin_username', 'admin')
    admin_password = data_dict.get('admin_password', 'administrator')
    admin = {
      'name': admin_username,
      'email': 'admin@localhost',
      'password': admin_password
    }
    toolkit.get_action('user_create')(context, admin)
    toolkit.get_action('user_patch')(context, {'id': admin['name'],
                                               'email': admin['email'],
                                               'sysadmin': True})

    return "Cleared"
