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
        # if categories is missing, remove groups
        data[key] = ""
        removed_keys = []
        for k in data.keys():
            if 'groups' in k:
                removed_keys.append(k)

        for k in removed_keys:
            data[k] = ""

    return data[key]
