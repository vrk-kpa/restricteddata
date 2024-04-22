from ckan.plugins import toolkit
from ckanext.dcat.profiles import (
    EuropeanDCATAP2Profile,
    XSD, RDF, DCT, DCAT, FOAF, ADMS, VCARD,
    Literal, URIRef, BNode)

from rdflib.namespace import Namespace

FREQUENCY = Namespace("http://publications.europa.eu/resource/authority/frequency/")

FREQUENCY_MAP = {
    "annual": "ANNUAL",
    "semiannual": "ANNUAL_2",
    "three_times_a_year": "ANNUAL_3",
    "bidecennial": "BIDECENNIAL",
    "biennial": "BIENNIAL",
    "bihourly": "BIHOURLY",
    "bimonthly": "BIMONTHLY",
    "biweekly": "BIWEEKLY",
    "continuous": "CONT",
    "daily": "DAILY",
    "twice_a_day": "DAILY_2",
    "decennial": "DECENNIAL",
    "hourly": "HOURLY",
    "irregular": "IRREG",
    "monthly": "MONTHLY",
    "semimonthly": "MONTHLY_2",
    "three_times_a_month": "MONTHLY_3",
    "never": "NEVER",
    "provisional_data": "OP_DATPRO",
    "other": "OTHER",
    "quadrennial": "QUADRENNIAL",
    "quarterly": "QUARTERLY",
    "quinquennial": "QUINQUENNIAL",
    "tridecennial": "TRIDECENNIAL",
    "triennial": "TRIENNIAL",
    "trihourly": "TRIHOURLY",
    "unknown": "UNKNOWN",
    "continuously_updated": "UPDATE_CONT",
    "weekly": "WEEKLY",
    "semiweekly": "WEEKLY_2",
    "three_times_a_week": "WEEKLY_3",
}


class RestrictedDataDCATAPProfile(EuropeanDCATAP2Profile):
    def parse_dataset(self, dataset_dict, dataset_ref):
        super().parse_dataset(dataset_dict, dataset_ref)
        return dataset_dict

    def graph_from_dataset(self, dataset_dict, dataset_ref):
        super().graph_from_dataset(dataset_dict, dataset_ref)

        self._add_fluent_text_fields(dataset_dict, dataset_ref, [
            ('title_translated', DCT.title),
            ('notes_translated', DCT.description),
            ('rights_translated', DCT.rights),
            ('keywords', DCAT.keyword),
        ])

        maintainer_website = dataset_dict.get('maintainer_website')
        if maintainer_website:
            contact_details = self.g.objects(subject=dataset_ref,
                                             predicate=DCAT.contactPoint)
            for node in contact_details:
                self.g.add((node, VCARD.hasUrl, URIRef(maintainer_website)))

        self._add_triple_from_dict(dataset_dict, dataset_ref, DCAT.landingPage,
                                   'external_urls', list_value=True, _type=URIRef)

        valid_from = dataset_dict.get('valid_from')
        valid_till = dataset_dict.get('valid_till')

        if valid_from or valid_till:
            temporal = BNode()
            self.g.add((dataset_ref, DCT.temporal, temporal))
            self.g.add((temporal, RDF.type, DCT.PeriodOfTime))
            self._add_triple_from_dict(dataset_dict, temporal, DCAT.startDate, 'valid_from', date_value=True)
            self._add_triple_from_dict(dataset_dict, temporal, DCAT.endDate, 'valid_till', date_value=True)

        update_frequency = dataset_dict.get('update_frequency')
        if update_frequency:
            self.g.bind("frequency", FREQUENCY)

            # update_frequency not existing in FREQUENCY_MAP is an error
            frequency = FREQUENCY[FREQUENCY_MAP[update_frequency]]
            self.g.add((dataset_ref, DCT.accrualPeriodicity, URIRef(frequency)))

        distributions = list(self.g.subjects(predicate=RDF.type, object=DCAT.Distribution))
        for distribution in distributions:
            resource_dict = next((r for r in dataset_dict.get('resources', [])
                                  if distribution.endswith(r['id'])), None)

            if resource_dict is None:
                continue

            self._add_fluent_text_fields(resource_dict, distribution, [
                ('name_translated', DCT.title),
                ('description_translated', DCT.description),
                ('rights_translated', DCT.rights),
                ('temporal_granularity', DCAT.temporalResolution),
            ])

            self._add_triple_from_dict(resource_dict, distribution, ADMS.status, 'maturity')
            self._add_triple_from_dict(resource_dict, distribution, DCAT.endpointUrl, 'endpoint_url', _type=URIRef)
            self._add_triple_from_dict(resource_dict, distribution, DCT.conformsTo, 'position_info')
            self._add_triple_from_dict(resource_dict, distribution, DCAT.spatialResolutionInMeters, 'geographical_accuracy')

            temporal_coverage_from = resource_dict.get('temporal_coverage_from')
            temporal_coverage_to = resource_dict.get('temporal_coverage_to')

            if temporal_coverage_from or temporal_coverage_to:
                temporal = BNode()
                self.g.add((distribution, DCT.temporal, temporal))
                self.g.add((temporal, RDF.type, DCT.PeriodOfTime))
                self._add_triple_from_dict(resource_dict, temporal, DCAT.startDate,
                                           'temporal_coverage_from', date_value=True)
                self._add_triple_from_dict(resource_dict, temporal, DCAT.endDate,
                                           'temporal_coverage_till', date_value=True)

            for size in self.g[distribution:DCAT.byteSize]:
                if size.datatype is not XSD.nonNegativeInteger:
                    self.g.remove((distribution, DCAT.byteSize, size))
                    value = Literal(int(size.value), datatype=XSD.nonNegativeInteger)
                    self.g.add((distribution, DCAT.byteSize, value))

        return dataset_dict

    def _add_fluent_text_fields(self, source_dict, ref, field_predicates):
        for field, predicate in field_predicates:
            self._add_fluent_text_field(source_dict, field, ref, predicate)

    def _add_fluent_text_field(self, source_dict, field, ref, predicate):
        field_value = self._get_dict_value(source_dict, field)
        for language, values in field_value.items():
            if not isinstance(values, list):
                values = [values]
            for value in values:
                if value:
                    self.g.add((ref, predicate, Literal(value, lang=language)))

    def graph_from_catalog(self, catalog_dict, catalog_ref):
        super(EuropeanDCATAP2Profile, self).graph_from_catalog(catalog_dict,
                                                               catalog_ref)

        # Catalog description is required, so add an empty one if it is missing
        if not list(self.g[catalog_ref:DCT.description]):
            self.g.add((catalog_ref, DCT.description, Literal('')))

        # Catalog publisher is required, so add it if it is missing
        if not list(self.g[catalog_ref:DCT.publisher]):
            publisher = BNode()
            self.g.add((publisher, RDF.type, FOAF.Organization))
            self.g.add((publisher, FOAF.hasSite,
                       URIRef(toolkit.config.get('ckan.site_url', ''))))
            names = [
                ('fi', 'Digi- ja väestötietovirasto'),
                ('sv', 'Myndigheten för digitalisering och befolkningsdata'),
                ('en', 'Digital and Population Data Services Agency'),
            ]
            for language, name in names:
                value = Literal(name, lang=language)
                self.g.add((publisher, FOAF.name, value))
            self.g.add((catalog_ref, DCT.publisher, publisher))
