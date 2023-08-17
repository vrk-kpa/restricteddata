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
# import ckanext.registrydata.plugin as plugin
from ckan.plugins import plugin_loaded
from ckantoolkit.tests.factories import Dataset, Sysadmin


@pytest.mark.usefixtures("with_plugins")
def test_plugin():
    assert plugin_loaded("registrydata")
    assert plugin_loaded("registrydata_pages")


@pytest.mark.usefixtures("clean_db", "with_plugins")
def test_insert_minimal_dataset():
    user = Sysadmin()
    Dataset(
        user=user,
        name='test-dataset',
        title_translated={'fi': 'Test', 'sv': 'Test'},
        notes_translated={'fi': 'Test', 'sv': 'Test'},
        access_rights='non-public',
        maintainer='maintainer',
        maintainer_email=['maintainer@example.com'],
        license_id='undefined',
        keywords={'fi': 'test', 'sv': 'test'},
        resources=[dict(
            url='http://example.com'
        )]
    )
