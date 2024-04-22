import pytest
import logging

from ckan.tests.factories import Dataset, Sysadmin, Organization
from ckan.tests.helpers import call_action
from ckan.plugins import toolkit
from .utils import minimal_dataset_with_one_resource_fields
from rdflib import Graph
from rdflib.term import Literal, URIRef
from rdflib.namespace import XSD
from urllib.parse import unquote

log = logging.getLogger(__name__)


def fetch_catalog_graph(app):
    with app.flask_app.test_request_context():
        app.flask_app.preprocess_request()
        data = call_action('dcat_catalog_show')

    log.warn(data)
    g = Graph()
    g.parse(data=data, format='application/rdf+xml')

    return g


@pytest.mark.usefixtures("clean_db", "clean_index", "with_plugins")
def test_dcat_catalog(app):
    catalog = fetch_catalog_graph(app).query('''
        SELECT ?title ?homepage
        WHERE {
            ?a a dcat:Catalog .
            ?a dcterms:title ?title .
            ?a foaf:homepage ?homepage
        }
        ''')

    [(title, homepage)] = list(catalog)
    assert title == Literal('CKAN')
    assert homepage == URIRef(toolkit.config.get('ckan.site_url'))


@pytest.mark.usefixtures("clean_db", "clean_index", "with_plugins")
def test_dcat_dataset_with_minimal_dataset(app):
    dataset_fields = minimal_dataset_with_one_resource_fields(Sysadmin())
    organization = Organization(name='org')
    dataset_fields['owner_org'] = organization['id']
    Dataset(**dataset_fields)

    result = fetch_catalog_graph(app).query('''
        SELECT ?id ?titleFi ?titleSv ?descriptionFi ?descriptionSv
               ?keywordFi ?keywordSv ?publisher
               ?accessRights ?maintainer ?maintainerEmail
        WHERE {
            ?a a dcat:Dataset
            . ?a dcterms:identifier ?id
            . ?a dcterms:title ?titleFi FILTER ( lang(?titleFi) = "fi")
            . ?a dcterms:title ?titleSv FILTER ( lang(?titleSv) = "sv")
            . ?a dcterms:description ?descriptionFi FILTER ( lang(?descriptionFi) = "fi")
            . ?a dcterms:description ?descriptionSv FILTER ( lang(?descriptionSv) = "sv")
            . ?a dcat:keyword ?keywordFi FILTER ( lang(?keywordFi) = "fi")
            . ?a dcat:keyword ?keywordSv FILTER ( lang(?keywordSv) = "sv")
            . ?a dcterms:publisher ?publisher
            . ?a dcterms:accessRights ?accessRights
            . ?a dcat:contactPoint ?contact
            . ?contact vcard:fn ?maintainer
            . ?contact vcard:hasEmail ?maintainerEmail
        }
        ''')

    [(id, title_fi, title_sv, notes_fi, notes_sv, keyword_fi, keyword_sv,
      publisher, access_rights, maintainer, maintainer_email)] = list(result)

    assert id is not None
    assert title_fi == Literal(dataset_fields['title_translated']['fi'], lang='fi')
    assert title_sv == Literal(dataset_fields['title_translated']['sv'], lang='sv')
    assert notes_fi == Literal(dataset_fields['notes_translated']['fi'], lang='fi')
    assert notes_sv == Literal(dataset_fields['notes_translated']['sv'], lang='sv')
    assert keyword_fi == Literal(dataset_fields['keywords']['fi'][0], lang='fi')
    assert keyword_sv == Literal(dataset_fields['keywords']['sv'][0], lang='sv')
    assert publisher is not None
    assert access_rights == Literal(dataset_fields['access_rights'])
    assert maintainer == Literal(dataset_fields['maintainer'])
    assert unquote(maintainer_email) == f'mailto:{dataset_fields["maintainer_email"]}'


@pytest.mark.usefixtures("clean_db", "clean_index", "with_plugins")
def test_dcat_dataset_rights(app):
    dataset_fields = minimal_dataset_with_one_resource_fields(Sysadmin())
    dataset_fields['rights_translated'] = {lang: f'rights {lang}'
                                           for lang in ['fi', 'sv', 'en']}
    Dataset(**dataset_fields)

    result = fetch_catalog_graph(app).query('''
        SELECT ?rightsFi ?rightsSv ?rightsEn
        WHERE {
            ?a a dcat:Dataset
            . ?a dcterms:rights ?rightsFi FILTER ( lang(?rightsFi) = "fi")
            . ?a dcterms:rights ?rightsSv FILTER ( lang(?rightsSv) = "sv")
            . ?a dcterms:rights ?rightsEn FILTER ( lang(?rightsEn) = "en")
        }
        ''')

    [(rights_fi, rights_sv, rights_en)] = list(result)

    assert rights_fi == Literal(dataset_fields['rights_translated']['fi'], lang='fi')
    assert rights_sv == Literal(dataset_fields['rights_translated']['sv'], lang='sv')
    assert rights_en == Literal(dataset_fields['rights_translated']['en'], lang='en')


@pytest.mark.usefixtures("clean_db", "clean_index", "with_plugins")
def test_dcat_dataset_maintainer_website(app):
    dataset_fields = minimal_dataset_with_one_resource_fields(Sysadmin())
    dataset_fields['maintainer_website'] = 'http://example.com'
    Dataset(**dataset_fields)

    result = fetch_catalog_graph(app).query('''
        SELECT ?maintainerWebsite
        WHERE {
            ?a a dcat:Dataset
            . ?a dcat:contactPoint ?contact
            . ?contact vcard:hasUrl ?maintainerWebsite
        }
        ''')

    [(maintainer_website,)] = list(result)

    assert maintainer_website == URIRef(dataset_fields['maintainer_website'])


@pytest.mark.usefixtures("clean_db", "clean_index", "with_plugins")
def test_dcat_dataset_external_urls(app):
    dataset_fields = minimal_dataset_with_one_resource_fields(Sysadmin())
    dataset_fields['external_urls'] = ['http://first.example.com',
                                       'http://second.example.com']
    Dataset(**dataset_fields)

    results = fetch_catalog_graph(app).query('''
        SELECT ?landingPage
        WHERE {
            ?a a dcat:Dataset
            . ?a dcat:landingPage ?landingPage
        }
        ''')

    external_urls = [result[0] for result in results]
    assert external_urls == [URIRef(url)
                             for url in dataset_fields['external_urls']]


@pytest.mark.usefixtures("clean_db", "clean_index", "with_plugins")
def test_dcat_dataset_update_frequency(app):
    dataset_fields = minimal_dataset_with_one_resource_fields(Sysadmin())
    dataset_fields['update_frequency'] = 'quarterly'
    Dataset(**dataset_fields)

    result = fetch_catalog_graph(app).query('''
        SELECT ?updateFrequency
        WHERE {
            ?a a dcat:Dataset
            . ?a dcterms:accrualPeriodicity ?updateFrequency
        }
        ''')

    [(update_frequency,)] = result
    assert update_frequency == URIRef('http://publications.europa.eu/resource/authority/frequency/QUARTERLY')


@pytest.mark.usefixtures("clean_db", "clean_index", "with_plugins")
def test_dcat_dataset_valid_from_till(app):
    dataset_fields = minimal_dataset_with_one_resource_fields(Sysadmin())
    dataset_fields['valid_from'] = '2023-01-01T00:00:00'
    dataset_fields['valid_till'] = '2033-01-01T00:00:00'
    Dataset(**dataset_fields)

    result = fetch_catalog_graph(app).query('''
        SELECT ?startDate ?endDate
        WHERE {
            ?a a dcat:Dataset
            . ?a dcterms:temporal ?temporal
            . ?temporal dcat:startDate ?startDate
            . ?temporal dcat:endDate ?endDate
        }
        ''')

    [(valid_from, valid_till)] = list(result)

    assert valid_from == Literal(dataset_fields['valid_from'], datatype=XSD.dateTime)
    assert valid_till == Literal(dataset_fields['valid_till'], datatype=XSD.dateTime)


@pytest.mark.usefixtures("clean_db", "clean_index", "with_plugins")
def test_dcat_resource_with_minimal_resource(app):
    dataset_fields = minimal_dataset_with_one_resource_fields(Sysadmin())
    resource_fields = dataset_fields['resources'][0]
    Dataset(**dataset_fields)

    result = fetch_catalog_graph(app).query('''
        SELECT ?url ?format ?size ?maturity ?rightsFi ?rightsSv
        WHERE {
            ?a a dcat:Distribution
            . ?a dcat:accessURL ?url
            . ?a dcterms:format ?format
            . ?a dcat:byteSize ?size
            . ?a adms:status ?maturity
            . ?a dcterms:rights ?rightsFi FILTER ( lang(?rightsFi) = "fi")
            . ?a dcterms:rights ?rightsSv FILTER ( lang(?rightsSv) = "sv")
        }
        ''')

    [(url, format, size, maturity, rights_fi, rights_sv)] = list(result)

    assert url == URIRef(resource_fields['url'])
    assert format == Literal(resource_fields['format'])
    assert size == Literal(resource_fields['size'], datatype=XSD.nonNegativeInteger)
    assert maturity == Literal(resource_fields['maturity'])
    assert rights_fi == Literal(resource_fields['rights_translated']['fi'], lang='fi')
    assert rights_sv == Literal(resource_fields['rights_translated']['sv'], lang='sv')


@pytest.mark.usefixtures("clean_db", "clean_index", "with_plugins")
def test_dcat_resource_with_name(app):
    dataset_fields = minimal_dataset_with_one_resource_fields(Sysadmin())
    resource_fields = dataset_fields['resources'][0]
    resource_fields['name_translated'] = {lang: f'Name {lang}' for lang in ['fi', 'sv', 'en']}
    Dataset(**dataset_fields)

    result = fetch_catalog_graph(app).query('''
        SELECT ?nameFi ?nameSv ?nameEn
        WHERE {
            ?a a dcat:Distribution
            . ?a dcterms:title ?nameFi FILTER ( lang(?nameFi) = "fi")
            . ?a dcterms:title ?nameSv FILTER ( lang(?nameSv) = "sv")
            . ?a dcterms:title ?nameEn FILTER ( lang(?nameEn) = "en")
        }
        ''')

    [(name_fi, name_sv, name_en)] = list(result)

    assert name_fi == Literal(resource_fields['name_translated']['fi'], lang='fi')
    assert name_sv == Literal(resource_fields['name_translated']['sv'], lang='sv')
    assert name_en == Literal(resource_fields['name_translated']['en'], lang='en')


@pytest.mark.usefixtures("clean_db", "clean_index", "with_plugins")
def test_dcat_resource_with_endpoint_url(app):
    dataset_fields = minimal_dataset_with_one_resource_fields(Sysadmin())
    resource_fields = dataset_fields['resources'][0]
    resource_fields['endpoint_url'] = 'https://example.com/endpoint'
    Dataset(**dataset_fields)

    result = fetch_catalog_graph(app).query('''
        SELECT ?endpointUrl
        WHERE {
            ?a a dcat:Distribution
            . ?a dcat:endpointUrl ?endpointUrl
        }
        ''')

    [(endpoint_url,)] = list(result)

    assert endpoint_url == URIRef(resource_fields['endpoint_url'])


@pytest.mark.usefixtures("clean_db", "clean_index", "with_plugins")
def test_dcat_resource_with_description(app):
    dataset_fields = minimal_dataset_with_one_resource_fields(Sysadmin())
    resource_fields = dataset_fields['resources'][0]
    resource_fields['description_translated'] = {lang: f'description {lang}'
                                                 for lang in ['fi', 'sv', 'en']}
    Dataset(**dataset_fields)

    result = fetch_catalog_graph(app).query('''
        SELECT ?descriptionFi ?descriptionSv ?descriptionEn
        WHERE {
            ?a a dcat:Distribution
            . ?a dcterms:description ?descriptionFi FILTER ( lang(?descriptionFi) = "fi")
            . ?a dcterms:description ?descriptionSv FILTER ( lang(?descriptionSv) = "sv")
            . ?a dcterms:description ?descriptionEn FILTER ( lang(?descriptionEn) = "en")
        }
        ''')

    [(description_fi, description_sv, description_en)] = list(result)

    assert description_fi == Literal(resource_fields['description_translated']['fi'], lang='fi')
    assert description_sv == Literal(resource_fields['description_translated']['sv'], lang='sv')
    assert description_en == Literal(resource_fields['description_translated']['en'], lang='en')


@pytest.mark.usefixtures("clean_db", "clean_index", "with_plugins")
def test_dcat_resource_with_position_info(app):
    dataset_fields = minimal_dataset_with_one_resource_fields(Sysadmin())
    resource_fields = dataset_fields['resources'][0]
    resource_fields['position_info'] = 'WGS84'
    Dataset(**dataset_fields)

    result = fetch_catalog_graph(app).query('''
        SELECT ?positionInfo
        WHERE {
            ?a a dcat:Distribution
            . ?a dcterms:conformsTo ?positionInfo
        }
        ''')

    [(position_info,)] = list(result)

    assert position_info == Literal(resource_fields['position_info'])


@pytest.mark.usefixtures("clean_db", "clean_index", "with_plugins")
def test_dcat_resource_with_temporal_granularity(app):
    dataset_fields = minimal_dataset_with_one_resource_fields(Sysadmin())
    resource_fields = dataset_fields['resources'][0]
    resource_fields['temporal_granularity'] = {lang: [f'temporal_granularity {lang} {x}'
                                               for x in range(2)] for lang in ['fi', 'sv', 'en']}
    Dataset(**dataset_fields)

    result = fetch_catalog_graph(app).query('''
        SELECT ?temporalGranularityFi ?temporalGranularitySv ?temporalGranularityEn
        WHERE {
            ?a a dcat:Distribution
            . ?a dcat:temporalResolution ?temporalGranularityFi FILTER ( lang(?temporalGranularityFi) = "fi")
            . ?a dcat:temporalResolution ?temporalGranularitySv FILTER ( lang(?temporalGranularitySv) = "sv")
            . ?a dcat:temporalResolution ?temporalGranularityEn FILTER ( lang(?temporalGranularityEn) = "en")
        }
        ''')

    results = [r for row in result for r in row]
    for lang, values in resource_fields['temporal_granularity'].items():
        for value in values:
            assert Literal(value, lang=lang) in results


@pytest.mark.usefixtures("clean_db", "clean_index", "with_plugins")
def test_dcat_resource_with_temporal_coverage(app):
    dataset_fields = minimal_dataset_with_one_resource_fields(Sysadmin())
    resource_fields = dataset_fields['resources'][0]
    resource_fields['temporal_coverage_from'] = '2023-01-01T00:00:00'
    resource_fields['temporal_coverage_till'] = '2033-01-01T00:00:00'
    Dataset(**dataset_fields)

    result = fetch_catalog_graph(app).query('''
        SELECT ?startDate ?endDate
        WHERE {
            ?a a dcat:Distribution
            . ?a dcterms:temporal ?temporal
            . ?temporal dcat:startDate ?startDate
            . ?temporal dcat:endDate ?endDate
        }
        ''')

    [(temporal_coverage_from, temporal_coverage_till)] = list(result)

    assert temporal_coverage_from == Literal(resource_fields['temporal_coverage_from'], datatype=XSD.dateTime)
    assert temporal_coverage_till == Literal(resource_fields['temporal_coverage_till'], datatype=XSD.dateTime)


@pytest.mark.usefixtures("clean_db", "clean_index", "with_plugins")
def test_dcat_resource_with_geographical_accuracy(app):
    dataset_fields = minimal_dataset_with_one_resource_fields(Sysadmin())
    resource_fields = dataset_fields['resources'][0]
    resource_fields['geographical_accuracy'] = 5
    Dataset(**dataset_fields)

    result = fetch_catalog_graph(app).query('''
        SELECT ?accuracy
        WHERE {
            ?a a dcat:Distribution
            . ?a dcat:spatialResolutionInMeters ?accuracy
        }
        ''')

    [(geographical_accuracy,)] = list(result)

    assert geographical_accuracy == Literal(resource_fields['geographical_accuracy'])
