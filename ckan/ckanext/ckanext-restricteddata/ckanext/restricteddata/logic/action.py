import datetime
import jwt
import random
import base64
import re

import ckan.model as model
from ckan.plugins import toolkit
from ckan.lib.munge import munge_title_to_name, substitute_ascii_equivalents
from ckan.types import Context, DataDict, Action
from ckanext.restricteddata.model import TemporaryMember, PahaAuthenticationToken
from logging import getLogger

log = getLogger(__name__)

# Adds new users to every group
@toolkit.chained_action
def user_create(original_action: Action, context: Context, data_dict: DataDict):
    result = original_action(context, data_dict)

    if result:
        context = {'ignore_auth': True}
        admin_user = toolkit.get_action('get_site_user')(context, None)
        context['user'] = admin_user['name']

        groups = toolkit.get_action('group_list')(context, {})

        for group in groups:
            member_data = {'id': group, 'username': result['name'], 'role': 'member'}
            toolkit.get_action('group_member_create')(context, member_data)

    return result


# Remove "member" capacity from UIs
@toolkit.side_effect_free
@toolkit.chained_action
def member_roles_list(original_action: Action, context: Context, data_dict: DataDict):
    roles = original_action(context, data_dict)

    group_type = data_dict.get('group_type', 'organization')
    if group_type == 'organization':
        result = [role for role in roles
                  if role['value'] != 'member']

    return result


def _decode_paha_jwt_token(encoded_token: str):
    '''Tries to decode a PAHA JWT token payload from request'''

    key = toolkit.config.get('ckanext.restricteddata.paha_jwt_key')
    algorithm = toolkit.config.get('ckanext.restricteddata.paha_jwt_algorithm')

    if not (key and algorithm and encoded_token):
        return

    try:
        token = jwt.decode(encoded_token, key, algorithms=[algorithm])
    except Exception:
        # Fallback to regular auth if anything at all goes wrong with the token
        return

    required_fields = ['iss', 'id', 'email', 'firstName', 'lastName', 'activeOrganizationId',
                       'activeOrganizationNameFi', 'activeOrganizationNameSv',
                       'activeOrganizationNameEn', 'expiresIn']
    if any(field not in token for field in required_fields):
        error = f'Token did not contain required fields: {", ".join(required_fields)}'
        raise toolkit.ValidationError(error)

    if token.get('iss') != 'PAHA':
        return

    return token


def _user_name_from_full_name(first_name, last_name):
    name = substitute_ascii_equivalents(f'{first_name}_{last_name}')
    name = name.lower()
    name = re.sub(r'\s', '-', name)
    name = re.sub(r'[^a-z0-9\-_]', '', name)

    max_name_creation_attempts = 100
    for _i in range(max_name_creation_attempts):
        number = random.randint(1, 100)
        user_name = f'{name}_{number}'
        if model.User.check_name_available(user_name):
            return user_name

    raise RuntimeError("Could not generate an available username!")


def _create_or_authenticate_paha_user(token: str):
    '''Identifies a user based on a PAHA JWT token creating a new user if needed'''
    user_id = token['id']
    user = model.User.get(user_id)

    # Create a new user if one does not exist
    if not user:
        toolkit.logout_user()
        user_email = token['email']
        user_first_name = token['firstName']
        user_last_name = token['lastName']
        user_name = _user_name_from_full_name(user_first_name, user_last_name)

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
        return user
    else:
        raise RuntimeError("Could not find or create PAHA user!")

def _create_or_get_paha_organization(token: str):
    '''Retrieves an organization based on a PAHA JWT token creating a new one if needed'''
    site_user_info = toolkit.get_action('get_site_user')({'ignore_auth': True}, {})
    organization_id = token['activeOrganizationId']
    try:
        context = {'ignore_auth': True}
        return toolkit.get_action('organization_show')(context, {'id': organization_id})

    except toolkit.ObjectNotFound:
        name_languages = ['fi', 'sv', 'en']
        fallback_language = 'fi'

        title_field = 'activeOrganizationName{}'.format
        organization_titles = {lang: (token[title_field(lang.capitalize())]
                                      or token[title_field(fallback_language.capitalize())])
                               for lang in name_languages}
        organization_title = next((organization_titles[lang]
                                  for lang in name_languages
                                  if organization_titles.get(lang)), None)
        if not organization_title:
            raise RuntimeError("Could not determine a non-empty name for PAHA organization!")

        existing_organization_names = set(toolkit.get_action('organization_list')({'ignore_auth': True}, {}))
        if len(existing_organization_names) >= 1000:
            log.error("Organization count over 1000, fix PAHA organization code")

        organization_name = munge_title_to_name(organization_title)
        for i in range(2, 100):
            if organization_name not in existing_organization_names:
                break
            else:
                organization_name = munge_title_to_name(f'{organization_title}-{i}')
        else:
            raise RuntimeError("Could not generate a unique name for organization!")

        organization_dict = {
            'id': organization_id,
            'name': organization_name,
            'title_translated': organization_titles,
            'image_url': ''
        }

        site_user_info = toolkit.get_action('get_site_user')({'ignore_auth': True}, {})
        context = {'user': site_user_info['name']}

        organization = toolkit.get_action('organization_create')(context, organization_dict)
        return organization


def authorize_paha_session(context: Context, data_dict: DataDict):
    '''Creates a temporary authentication token based on a valid PAHA JWT.'''
    toolkit.check_access('sysadmin', context)
    encoded_token = data_dict.get('token')
    paha_jwt_token = _decode_paha_jwt_token(encoded_token)
    if not paha_jwt_token:
        log.error("No valid PAHA JWT provided")
        return toolkit.abort(400)

    user = _create_or_authenticate_paha_user(paha_jwt_token)
    organization = _create_or_get_paha_organization(paha_jwt_token)
    # expiresIn is a timestamp expressed in milliseconds
    expires = datetime.datetime.fromtimestamp(paha_jwt_token['expiresIn'] / 1000)

    toolkit.get_action('grant_temporary_membership')({'ignore_auth': True}, {
        'user': user.id,
        'organization': organization['id'],
        'expires': expires
    })

    token = PahaAuthenticationToken(user.id, expires)
    session = context['session']
    session.add(token)
    session.commit()
    return token.secret


def purge_expired_paha_auth_tokens(context: Context, data_dict: DataDict):
    '''Removes expired PAHA authentication token entries from the database'''
    toolkit.check_access('sysadmin', context)
    PahaAuthenticationToken.purge_expired()


def grant_temporary_membership(context: Context, data_dict: DataDict):
    '''Creates a temporary organization admin membership for the user and marks it for removal after expiry.'''
    toolkit.check_access('sysadmin', context)
    session = context['session']
    user_id = toolkit.get_or_bust(data_dict, 'user')
    organization_id = toolkit.get_or_bust(data_dict, 'organization')
    expires = toolkit.get_or_bust(data_dict, 'expires')

    TemporaryMember.purge_expired()
    temporary_member = TemporaryMember.get(user_id, organization_id)
    if temporary_member is None:
        member = toolkit.get_action('member_create')({"ignore_auth": True}, {
                                                         "id": organization_id,
                                                         "object": user_id,
                                                         "object_type": "user",
                                                         "capacity": "admin"
                                                     })
        temporary_member = TemporaryMember(user_id, organization_id, expires, member["id"])
    else:
        temporary_member.expires = expires

    session.add(temporary_member)
    session.commit()


def purge_expired_temporary_memberships(context: Context, data_dict: DataDict):
    '''Removes expired temporary memberships from the database'''
    toolkit.check_access('sysadmin', context)
    TemporaryMember.purge_expired()


@toolkit.side_effect_free
@toolkit.chained_action
def user_autocomplete(original_action: Action, context: Context, data_dict: DataDict):
    try:
        toolkit.check_access('user_autocomplete', context, data_dict)
    except toolkit.NotAuthorized:
        return []

    return original_action(context, data_dict)


@toolkit.side_effect_free
@toolkit.chained_action
def member_list(original_action: Action, context: Context, data_dict: DataDict):
    data_dict['object_type'] = data_dict.get('object_type', 'package')
    return original_action(context, data_dict)
