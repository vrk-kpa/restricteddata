from ckan.plugins import toolkit
from ckanext.restricteddata.model import TemporaryMember

# Adds new users to every group
@toolkit.chained_action
def user_create(original_action, context, data_dict):
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
@toolkit.chained_action
def member_roles_list(original_action, context, data_dict):
    roles = original_action(context, data_dict)

    group_type = data_dict.get('group_type', 'organization')
    if group_type == 'organization':
        result = [role for role in roles
                  if role['value'] != 'member']

    return result


def grant_temporary_membership(context, data_dict):
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


def purge_expired_temporary_memberships(context, data_dict):
    toolkit.check_access('sysadmin', context)
    TemporaryMember.purge_expired()
