from ckanext.dcat.profiles import EuropeanDCATAP2Profile


class RegistrydataDCATAPProfile(EuropeanDCATAP2Profile):
    def parse_dataset(self, dataset_dict, dataset_ref):
        super().parse_dataset(dataset_dict, dataset_ref)
        return dataset_dict

    def graph_from_dataset(self, dataset_dict, dataset_ref):
        super().graph_from_dataset(dataset_dict, dataset_ref)
        return dataset_dict
