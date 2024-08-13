import pytest

# import ckanext.restricteddata.plugin as plugin
from ckan.plugins import toolkit
from ckan.tests.factories import Dataset, Sysadmin, Organization, User, Group
from .utils import minimal_dataset_with_one_resource_fields

import ckanext.restricteddata.helpers as helpers


@pytest.mark.usefixtures("clean_db", "with_plugins")
class TestGetAssignableGroupsForPackageHelper(object):
    @pytest.mark.usefixtures("with_request_context")
    def test_get_assignable_groups_for_package_helper_with_non_maintainer(self, app):
        _g = Group()
        some_user = User()
        org = Organization()

        dataset_fields = minimal_dataset_with_one_resource_fields(Sysadmin())
        dataset_fields['owner_org'] = org['id']
        d = Dataset(**dataset_fields)

        toolkit.g.user = some_user['name']
        groups = helpers.get_assignable_groups_for_package(d)
        assert groups == []

    @pytest.mark.usefixtures("with_request_context")
    def test_get_assignable_groups_for_package_helper_with_maintainer(self, app):
        g1 = Group()
        g2 = Group()
        maintainer = User()
        org = Organization(user=maintainer)

        dataset_fields = minimal_dataset_with_one_resource_fields(Sysadmin())
        dataset_fields['owner_org'] = org['id']
        dataset_fields['categories'] = [g1['name']]
        d = Dataset(**dataset_fields)

        toolkit.g.user = maintainer['name']
        [unassigned_group] = helpers.get_assignable_groups_for_package(d)
        assert unassigned_group['name'] == g2['name']


@pytest.mark.usefixtures("clean_db", "with_plugins")
def test_get_group_title_translations():
    titles = [(lang, f'title {lang}') for lang in ['fi', 'sv', 'en']]
    g = Group(title_translated=dict(titles))
    name = g['name']
    group_titles = helpers.get_group_title_translations()

    for lang, title in titles:
        assert group_titles[name][lang] == title


@pytest.mark.usefixtures("clean_db", "with_plugins")
def test_get_translated_groups():
    titles = [(lang, f'title {lang}') for lang in ['fi', 'sv', 'en']]
    g = Group(title_translated=dict(titles))
    del g['title_translated']
    [translated] = helpers.get_translated_groups([g])

    for lang, title in titles:
        assert translated['title_translated'][lang] == title
