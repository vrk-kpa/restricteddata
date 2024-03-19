from ckan.plugins import toolkit


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
