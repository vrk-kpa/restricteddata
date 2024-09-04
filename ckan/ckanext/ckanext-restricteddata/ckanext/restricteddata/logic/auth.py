from ckan.plugins import toolkit
from ckan.types import Context, DataDict, AuthResult, AuthFunction

@toolkit.chained_auth_function
def member_create(next_auth: AuthFunction, context: Context, data_dict: DataDict) -> AuthResult:
    if data_dict['object_type'] == 'package':
        try:
            toolkit.check_access('package_update', context, {'id': data_dict['object']})
        except toolkit.NotAuthorized:
            return {'success': False,
                    'message': 'Only dataset owners can modify dataset groups'}

    return next_auth(context, data_dict)

@toolkit.chained_auth_function
def member_delete(next_auth: AuthFunction, context: Context, data_dict: DataDict) -> AuthResult:
    if data_dict['object_type'] == 'package':
        try:
            toolkit.check_access('package_update', context, {'id': data_dict['object']})
        except toolkit.NotAuthorized:
            return {'success': False,
                    'message': 'Only dataset owners can modify dataset groups'}

    return next_auth(context, data_dict)


def sysadmin_only(contaxt, data_dict):
    return {'success': False, 'message': 'Only sysadmins are allowed to call this'}
