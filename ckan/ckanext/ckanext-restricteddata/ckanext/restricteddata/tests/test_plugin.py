"""
Tests for plugin.py.

Tests are written using the pytest library (https://docs.pytest.org), and you
should read the testing guidelines in the CKAN docs:
https://docs.ckan.org/en/2.9/contributing/testing.html

To write tests for your extension you should install the pytest-ckan package:

    pip install pytest-ckan

This will allow you to use CKAN specific fixtures on your tests.

For instance, if your test involves database access you can use `clean_db` to
reset the database:

    import pytest

    from ckan.tests import factories

    @pytest.mark.usefixtures("clean_db")
    def test_some_action():

        dataset = factories.Dataset()

        # ...

For functional tests that involve requests to the application, you can use the
`app` fixture:

    from ckan.plugins import toolkit

    def test_some_endpoint(app):

        url = toolkit.url_for('myblueprint.some_endpoint')

        response = app.get(url)

        assert response.status_code == 200


To temporary patch the CKAN configuration for the duration of a test you can use:

    import pytest

    @pytest.mark.ckan_config("ckanext.myext.some_key", "some_value")
    def test_some_action():
        pass
"""
import pytest

# import ckanext.restricteddata.plugin as plugin
from ckan.plugins import plugin_loaded, toolkit
from ckan.tests.factories import Dataset, Sysadmin, Organization, User, Group
from ckan.tests.helpers import call_action
from .utils import minimal_dataset_with_one_resource_fields


@pytest.mark.usefixtures("with_plugins")
def test_plugin():
    assert plugin_loaded("restricteddata")
    assert plugin_loaded("restricteddata_pages")


@pytest.mark.usefixtures("clean_db", "clean_index", "with_plugins")
def test_minimal_dataset():
    dataset_fields = minimal_dataset_with_one_resource_fields(Sysadmin())
    Dataset(**dataset_fields)

    datasets = call_action('package_search', q='')['results']
    assert len(datasets) == 1
    dataset = datasets[0]

    assert dataset['title'] == dataset_fields['title_translated']['fi']
    assert dataset['title_translated'] == dataset_fields['title_translated']
    assert dataset['notes'] == dataset_fields['notes_translated']['fi']
    assert dataset['notes_translated'] == dataset_fields['notes_translated']
    assert dataset['access_rights'] == dataset_fields['access_rights']
    assert dataset['maintainer'] == dataset_fields['maintainer']
    assert dataset['maintainer_email'] == dataset_fields['maintainer_email']
    assert dataset['license_id'] == dataset_fields['license_id']
    assert dataset['keywords'] == dataset_fields['keywords']

    assert len(dataset['resources']) == 1
    resource = dataset['resources'][0]
    assert resource['url'] == dataset_fields['resources'][0]['url']


@pytest.mark.usefixtures("clean_db", "with_plugins")
def test_dataset_with_rights():
    dataset_fields = minimal_dataset_with_one_resource_fields(Sysadmin())
    dataset_fields['rights_translated'] = {'fi': 'Test', 'sv': 'Test'}
    d = Dataset(**dataset_fields)
    dataset = call_action('package_show', id=d['name'])
    assert dataset['rights_translated'] == dataset_fields['rights_translated']


@pytest.mark.usefixtures("clean_db", "with_plugins")
def test_dataset_with_maintainer_website():
    dataset_fields = minimal_dataset_with_one_resource_fields(Sysadmin())
    dataset_fields['maintainer_website'] = 'http://example.com'
    d = Dataset(**dataset_fields)
    dataset = call_action('package_show', id=d['name'])
    assert dataset['maintainer_website'] == dataset_fields['maintainer_website']


@pytest.mark.usefixtures("clean_db", "with_plugins")
def test_dataset_with_highvalue():
    dataset_fields = minimal_dataset_with_one_resource_fields(Sysadmin())
    dataset_fields['highvalue'] = True
    d = Dataset(**dataset_fields)
    dataset = call_action('package_show', id=d['name'])
    assert dataset['highvalue'] == 'true'


@pytest.mark.usefixtures("clean_db", "with_plugins")
def test_dataset_with_external_ursl():
    dataset_fields = minimal_dataset_with_one_resource_fields(Sysadmin())
    dataset_fields['external_urls'] = ['http://example.com', 'https://example.com']
    d = Dataset(**dataset_fields)
    dataset = call_action('package_show', id=d['name'])
    assert dataset['external_urls'] == dataset_fields['external_urls']


@pytest.mark.usefixtures("clean_db", "with_plugins")
def test_dataset_with_update_frequency():
    dataset_fields = minimal_dataset_with_one_resource_fields(Sysadmin())
    dataset_fields['update_frequency'] = 'quarterly'
    d = Dataset(**dataset_fields)
    dataset = call_action('package_show', id=d['name'])
    assert dataset['update_frequency'] == dataset_fields['update_frequency']

    dataset_fields['update_frequency'] = 'invalid value'
    with pytest.raises(toolkit.ValidationError):
        d = Dataset(**dataset_fields)


@pytest.mark.usefixtures("clean_db", "with_plugins")
def test_dataset_with_valid_from():
    dataset_fields = minimal_dataset_with_one_resource_fields(Sysadmin())
    dataset_fields['valid_from'] = '2023-01-01'
    d = Dataset(**dataset_fields)
    dataset = call_action('package_show', id=d['name'])
    assert dataset['valid_from'] == dataset_fields['valid_from']


@pytest.mark.usefixtures("clean_db", "with_plugins")
def test_dataset_with_valid_till():
    dataset_fields = minimal_dataset_with_one_resource_fields(Sysadmin())
    dataset_fields['valid_till'] = '2033-01-01'
    d = Dataset(**dataset_fields)
    dataset = call_action('package_show', id=d['name'])
    assert dataset['valid_till'] == dataset_fields['valid_till']


@pytest.mark.usefixtures("clean_db", "with_plugins")
def test_dataset_with_resource_with_name():
    dataset_fields = minimal_dataset_with_one_resource_fields(Sysadmin())
    dataset_fields['resources'][0]['name_translated'] = {'fi': 'Test',
                                                         'sv': 'Test'}
    d = Dataset(**dataset_fields)
    dataset = call_action('package_show', id=d['name'])
    resource = dataset['resources'][0]
    assert resource['name_translated'] == dataset_fields['resources'][0]['name_translated']


@pytest.mark.usefixtures("clean_db", "with_plugins")
def test_dataset_with_resource_with_format():
    dataset_fields = minimal_dataset_with_one_resource_fields(Sysadmin())
    dataset_fields['resources'][0]['format'] = 'CSV'
    d = Dataset(**dataset_fields)
    dataset = call_action('package_show', id=d['name'])
    resource = dataset['resources'][0]
    assert resource['format'] == dataset_fields['resources'][0]['format']


@pytest.mark.usefixtures("clean_db", "with_plugins")
def test_dataset_with_resource_with_size():
    dataset_fields = minimal_dataset_with_one_resource_fields(Sysadmin())
    dataset_fields['resources'][0]['size'] = 31415
    d = Dataset(**dataset_fields)
    dataset = call_action('package_show', id=d['name'])
    resource = dataset['resources'][0]
    assert resource['size'] == dataset_fields['resources'][0]['size']


@pytest.mark.usefixtures("clean_db", "with_plugins")
def test_dataset_with_resource_with_rights():
    dataset_fields = minimal_dataset_with_one_resource_fields(Sysadmin())
    dataset_fields['resources'][0]['rights_translated'] = {'fi': 'Test',
                                                           'sv': 'Test'}
    d = Dataset(**dataset_fields)
    dataset = call_action('package_show', id=d['name'])
    resource = dataset['resources'][0]
    assert resource['rights_translated'] == dataset_fields['resources'][0]['rights_translated']


@pytest.mark.usefixtures("clean_db", "with_plugins")
def test_dataset_with_private_resource_not_showing_for_unauthorized_user(app):
    dataset_fields = minimal_dataset_with_one_resource_fields(Sysadmin())
    author = User()
    org = Organization(user=author)
    dataset_fields['owner_org'] = org['id']
    dataset_fields['resources'][0]['private'] = True
    d = Dataset(**dataset_fields)

    user = User()
    with app.flask_app.test_request_context():
        app.flask_app.preprocess_request()
        public_dataset = call_action('package_show', id=d['name'],
                                     context={'user': user['name'],
                                              'ignore_auth': False})
        assert len(public_dataset['resources']) == 0


@pytest.mark.usefixtures("clean_db", "with_plugins")
def test_dataset_with_resource_with_private(app):
    dataset_fields = minimal_dataset_with_one_resource_fields(Sysadmin())
    author = User()
    org = Organization(user=author)
    dataset_fields['owner_org'] = org['id']
    dataset_fields['resources'][0]['private'] = True
    d = Dataset(**dataset_fields)

    with app.flask_app.test_request_context():
        app.flask_app.preprocess_request()
        dataset = call_action('package_show', id=d['name'],
                              context={'user': author['name'],
                                       'ignore_auth': False})
        resource = dataset['resources'][0]
        assert resource['private'] == dataset_fields['resources'][0]['private']


@pytest.mark.usefixtures("clean_db", "with_plugins")
def test_dataset_with_resource_with_maturity():
    dataset_fields = minimal_dataset_with_one_resource_fields(Sysadmin())
    dataset_fields['resources'][0]['maturity'] = 'current'
    d = Dataset(**dataset_fields)
    dataset = call_action('package_show', id=d['name'])
    resource = dataset['resources'][0]
    assert resource['maturity'] == dataset_fields['resources'][0]['maturity']


@pytest.mark.usefixtures("clean_db", "with_plugins")
def test_dataset_with_resource_with_description():
    dataset_fields = minimal_dataset_with_one_resource_fields(Sysadmin())
    dataset_fields['resources'][0]['description_translated'] = {'fi': 'Test',
                                                                'sv': 'Test'}
    d = Dataset(**dataset_fields)
    dataset = call_action('package_show', id=d['name'])
    resource = dataset['resources'][0]
    assert resource['description_translated'] == dataset_fields['resources'][0]['description_translated']


@pytest.mark.usefixtures("clean_db", "with_plugins")
def test_dataset_with_resource_with_position_info():
    dataset_fields = minimal_dataset_with_one_resource_fields(Sysadmin())
    dataset_fields['resources'][0]['position_info'] = 'WGS84'
    d = Dataset(**dataset_fields)
    dataset = call_action('package_show', id=d['name'])
    resource = dataset['resources'][0]
    assert resource['position_info'] == dataset_fields['resources'][0]['position_info']


@pytest.mark.usefixtures("clean_db", "with_plugins")
def test_dataset_with_resource_with_temporal_granularity():
    dataset_fields = minimal_dataset_with_one_resource_fields(Sysadmin())
    dataset_fields['resources'][0]['temporal_granularity'] = {'fi': ['Test'],
                                                              'sv': ['Test']}
    d = Dataset(**dataset_fields)
    dataset = call_action('package_show', id=d['name'])
    resource = dataset['resources'][0]
    assert resource['temporal_granularity'] == dataset_fields['resources'][0]['temporal_granularity']


@pytest.mark.usefixtures("clean_db", "with_plugins")
def test_dataset_with_resource_with_temporal_coverage_from():
    dataset_fields = minimal_dataset_with_one_resource_fields(Sysadmin())
    dataset_fields['resources'][0]['temporal_coverage_from'] = '2023-01-01'
    d = Dataset(**dataset_fields)
    dataset = call_action('package_show', id=d['name'])
    resource = dataset['resources'][0]
    assert resource['temporal_coverage_from'] == dataset_fields['resources'][0]['temporal_coverage_from']


@pytest.mark.usefixtures("clean_db", "with_plugins")
def test_dataset_with_resource_with_temporal_coverage_till():
    dataset_fields = minimal_dataset_with_one_resource_fields(Sysadmin())
    dataset_fields['resources'][0]['temporal_coverage_till'] = '2033-01-01'
    d = Dataset(**dataset_fields)
    dataset = call_action('package_show', id=d['name'])
    resource = dataset['resources'][0]
    assert resource['temporal_coverage_till'] == dataset_fields['resources'][0]['temporal_coverage_till']


@pytest.mark.usefixtures("clean_db", "with_plugins")
def test_dataset_with_resource_with_geographical_accuracy():
    dataset_fields = minimal_dataset_with_one_resource_fields(Sysadmin())
    dataset_fields['resources'][0]['geographical_accuracy'] = 5
    d = Dataset(**dataset_fields)
    dataset = call_action('package_show', id=d['name'])
    resource = dataset['resources'][0]
    assert resource['geographical_accuracy'] == dataset_fields['resources'][0]['geographical_accuracy']


@pytest.mark.usefixtures("clean_db", "with_plugins")
def test_user_can_add_dataset_to_group(app):
    g = Group()
    author = User()
    org = Organization(user=author)

    dataset_fields = minimal_dataset_with_one_resource_fields(Sysadmin())
    dataset_fields['owner_org'] = org['id']
    d = Dataset(**dataset_fields)

    with app.flask_app.test_request_context():
        app.flask_app.preprocess_request()
        # Add dataset d to group g
        member = call_action('member_create', id=g['id'], object=d['id'],
                             object_type='package', capacity='parent',
                             context={'user': author['name'], 'ignore_auth': False})
        print(member)
        assert member['group_id'] == g['id']
        assert member['table_id'] == d['id']
        assert member['table_name'] == 'package'
        assert member['capacity'] == 'parent'
