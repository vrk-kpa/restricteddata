from ckan.plugins import toolkit

@toolkit.chained_auth_function
def member_create(next_auth, context, data_dict):
    if data_dict['object_type'] == 'package':
        try:
            toolkit.check_access('package_update', context, {'id': data_dict['object']})
        except toolkit.NotAuthorized:
            return {'success': False,
                    'message': 'Only dataset owners can modify dataset groups'}

    return next_auth(context, data_dict)

@toolkit.chained_auth_function
def member_delete(next_auth, context, data_dict):
    if data_dict['object_type'] == 'package':
        try:
            toolkit.check_access('package_update', context, {'id': data_dict['object']})
        except toolkit.NotAuthorized:
            return {'success': False,
                    'message': 'Only dataset owners can modify dataset groups'}

    return next_auth(context, data_dict)
