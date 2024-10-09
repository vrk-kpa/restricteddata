import pytest

# import ckanext.restricteddata.plugin as plugin
from ckan.plugins import toolkit
from ckan.tests.factories import Dataset, Sysadmin, User, Group
from .utils import minimal_dataset_with_one_resource_fields, minimal_group

import ckanext.restricteddata.helpers as helpers
from .factories import RestrictedDataOrganization

@pytest.mark.usefixtures("with_plugins", "clean_db")
class TestGetAssignableGroupsForPackageHelper(object):
    @pytest.mark.usefixtures("with_request_context")
    def test_get_assignable_groups_for_package_helper_with_non_maintainer(self, app):
        _g = Group(**minimal_group())
        some_user = User()
        org = RestrictedDataOrganization()

        dataset_fields = minimal_dataset_with_one_resource_fields(Sysadmin())
        dataset_fields['owner_org'] = org['id']
        d = Dataset(**dataset_fields)

        toolkit.g.user = some_user['name']
        groups = helpers.get_assignable_groups_for_package(d)
        assert groups == []

    @pytest.mark.usefixtures("with_request_context")
    def test_get_assignable_groups_for_package_helper_with_maintainer(self, app):
        g1 = Group(**minimal_group())
        g2 = Group(**minimal_group())
        maintainer = User()
        org = RestrictedDataOrganization(user=maintainer)

        dataset_fields = minimal_dataset_with_one_resource_fields(Sysadmin())
        dataset_fields['owner_org'] = org['id']
        dataset_fields['groups'] = [{'name': g1['name']}]
        d = Dataset(**dataset_fields)

        toolkit.g.user = maintainer['name']
        [unassigned_group] = helpers.get_assignable_groups_for_package(d)
        assert unassigned_group['name'] == g2['name']


@pytest.mark.usefixtures("with_plugins", "clean_db")
def test_get_group_title_translations():
    titles = [(lang, f'title {lang}') for lang in ['fi', 'sv', 'en']]
    g = Group(title_translated=dict(titles))
    name = g['name']
    group_titles = helpers.get_group_title_translations()

    for lang, title in titles:
        assert group_titles[name][lang] == title


@pytest.mark.usefixtures("with_plugins", "clean_db")
def test_get_translated_groups():
    titles = [(lang, f'title {lang}') for lang in ['fi', 'sv', 'en']]
    g = Group(title_translated=dict(titles))
    del g['title_translated']
    [translated] = helpers.get_translated_groups([g])

    for lang, title in titles:
        assert translated['title_translated'][lang] == title
