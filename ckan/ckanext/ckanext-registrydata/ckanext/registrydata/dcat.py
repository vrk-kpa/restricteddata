from ckanext.dcat.profiles import EuropeanDCATAP2Profile, RDF, DCT, DCAT, ADMS, VCARD, Literal, URIRef, BNode


class RegistrydataDCATAPProfile(EuropeanDCATAP2Profile):
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
            ('update_frequency', DCT.accrualPeriodicity),
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

