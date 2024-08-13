import json
from ckan.lib.navl.dictization_functions import missing, flatten_list

def save_to_groups(key, data, errors, context):
    # https://docs.ckan.org/en/ckan-2.7.3/api/#ckan.logic.action.create.package_create
    # Add selected items as groups to dataset
    value = data[key]

    if value and value is not missing:

        if isinstance(value, str):
            group_patch = flatten_list([{"name": value}])
            group_key = ('groups',) + list(group_patch.keys())[0]
            group_value = list(group_patch.values())[0]
            data[group_key] = group_value
        else:
            if isinstance(value, list):
                data[key] = json.dumps(value)
                groups_with_details = []
                for identifier in value:
                    groups_with_details.append({"name": identifier})
                group_patch = flatten_list(groups_with_details)

                for k, v in group_patch.items():
                    group_key = ('groups',) + k
                    data[group_key] = v

    else:
        # Convert categories and groups key values to empty string if categories key is missing
        data[key] = ""
        data[('groups',)] = ""

    return data[key]


def highvalue(key, data, errors, context):
    value = data[key]

    # Remove highvalue categories if highvalue is false
    if value is False:
        removed_keys = []
        for k in data.keys():
            if 'highvalue_category' in k:
                removed_keys.append(k)

        for k in removed_keys:
            data[k] = []
