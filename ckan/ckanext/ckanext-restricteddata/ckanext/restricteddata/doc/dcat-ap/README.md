# Suomi.fi Restricted Data DCAT-AP extension

## Validation

Documents can be validated against this specification with a [SHACL](https://www.w3.org/TR/shacl/) processor using these schema files:

- [restricteddata_dcat-ap_shacl.ttl](restricteddata_dcat-ap_shacl.ttl)
- [FOAF.ttl](FOAF.ttl)

For example, using [pyshacl](https://pypi.org/project/pyshacl):

    pyshacl -s restricteddata_dcat-ap_shacl.ttl -e FOAF.ttl --imports -i rdfs catalog.xml

## Vocabularies

Prefix | URI
-------|----
adms | http://www.w3.org/ns/adms#
dcat | http://www.w3.org/ns/dcat#
dcatap | http://data.europa.eu/r5r/
dct | http://purl.org/dc/terms/
foaf | http://xmlns.com/foaf/0.1/
locn | http://www.w3.org/ns/locn#
owl | http://www.w3.org/2002/07/owl#
odrl | http://www.w3.org/ns/odrl/2/
rdfs | http://www.w3.org/2000/01/rdf-schema#
schema | http://schema.org/
skos | http://www.w3.org/2004/02/skos/core#
spdx | http://spdx.org/rdf/terms#
xsd | http://www.w3.org/2001/XMLSchema#
vann | http://purl.org/vocab/vann/
voaf | http://purl.org/vocommons/voaf#
vcard | http://www.w3.org/2006/vcard/ns#
geodcat | http://data.europa.eu/930/#
gsp | http://www.opengis.net/ont/geosparql#
hvd | https://semiceu.github.io/uri.semic.eu-generated/DCAT-AP/releases/2.2.0-hvd/#


## Classes


### Catalog

#### Catalogue

A catalogue or repository that hosts the Datasets being described.

#### Properties



##### Mandatory
Term | Range | Cardinality | Comment
-----|-------|-------------|--------
dcat:dataset | dcat:Dataset | 1..n | This property links the Catalogue with a Dataset that is part of the Catalogue.
dct:description | rdfs:Literal | 1..n | This property contains a free-text account of the Catalogue. This property can be repeated for parallel language versions of the description. For further information on multilingual issues, please refer to section 8.
dct:publisher | foaf:Agent | 1..1 | This property refers to an entity (organisation) responsible for making the Catalogue available.
dct:title | rdfs:Literal | 1..n | This property contains a name given to the Catalogue. This property can be repeated for parallel language versions of the name.
 



##### Recommended
Term | Range | Cardinality | Comment
-----|-------|-------------|--------
foaf:homepage | foaf:Document | 0..1 | This property refers to a web page that acts as the main page for the Catalogue.
dct:language | dct:LinguisticSystem | 0..n | This property refers to a language used in the textual metadata describing titles, descriptions, etc. of the Datasets in the Catalogue. This property can be repeated if the metadata is provided in multiple languages.
 



 

### Dataset

#### Dataset

A conceptual entity that represents the information published.

#### Properties



##### Mandatory
Term | Range | Cardinality | Comment
-----|-------|-------------|--------
dct:description | rdfs:Literal | 1..n | This property contains a free-text account of the Dataset. This property can be repeated for parallel language versions of the description.
dct:title | rdfs:Literal | 1..n | This property contains a name given to the Dataset. This property can be repeated for parallel language versions of the name.
 



##### Recommended
Term | Range | Cardinality | Comment
-----|-------|-------------|--------
dcat:contactPoint | vcard:Kind | 0..n | This property contains contact information that can be used for sending comments about the Dataset.
dcat:distribution | dcat:Distribution | 0..n | This property links the Dataset to an available Distribution.
dcat:keyword | rdfs:Literal | 0..n | This property contains a keyword or tag describing the Dataset.
dct:publisher | foaf:Agent | 0..1 | This property refers to an entity (organisation) responsible for making the Dataset available.
dct:spatial | dct:Location | 0..n | This property refers to a geographic region that is covered by the Dataset.
dct:temporal | dct:PeriodOfTime | 0..1 | This property refers to a temporal period that the Dataset covers.
dcat:theme, subproperty of dct:subject | skos:Concept | 0..n | This property refers to a category of the Dataset. A Dataset may be associated with multiple themes.
 



##### Optional
Term | Range | Cardinality | Comment
-----|-------|-------------|--------
dct:accessRights | dct:RightsStatement | 0..1 | This property refers to information that indicates whether the Dataset is open data, has access restrictions or is not public. A controlled vocabulary with three members (:public, :restricted, :non-public) will be created and maintained by the Publications Office of the EU.
dct:accrualPeriodicity | dct:Frequency | 0..1 | This property refers to the frequency at which the Dataset is updated.
dct:identifier | rdfs:Literal | 0..n | This property contains the main identifier for the Dataset, e.g. the URI or other unique identifier in the context of the Catalogue.
dcat:landingPage | foaf:Document | 0..n | This property refers to a web page that provides access to the Dataset, its Distributions and/or additional information. It is intended to point to a landing page at the original data provider, not to a page on a site of a third party, such as an aggregator.
dct:issued | rdfs:Literal typed as xsd:date or xsd:dateTime | 0..1 | This property contains the date of formal issuance (e.g., publication) of the Dataset.
dct:type | skos:Concept | 0..1 | This property refers to the type of the Dataset. A controlled vocabulary for the values has not been established.
dct:modified | rdfs:Literal typed as xsd:date or xsd:dateTime | 0..1 | This property contains the most recent date on which the Dataset was changed or modified.
dcatap:hvdCategory | skos:Concept | 0..n | The HVD category to which this Dataset belongs.
dcatap:applicableLegislation | hvd:LegalResource | 0..n | The legislation that mandates the creation or management of the Dataset.
 

 

### Distribution

#### Distribution

A physical embodiment of the Dataset in a particular format.

#### Properties



##### Mandatory
Term | Range | Cardinality | Comment
-----|-------|-------------|--------
dcat:accessURL | rdfs:Resource | 1..n | This property contains a URL that gives access to a Distribution of the Dataset. The resource at the access URL may contain information about how to get the Dataset.
 



##### Recommended
Term | Range | Cardinality | Comment
-----|-------|-------------|--------
dct:description | rdfs:Literal | 0..n | This property contains a free-text account of the Distribution. This property can be repeated for parallel language versions of the description.
dct:format | dct:MediaTypeOrExtent | 0..1 | This property refers to the file format of the Distribution.
dct:license | dct:LicenseDocument | 0..1 | This property refers to the licence under which the Distribution is made available.
 



##### Optional
Term | Range | Cardinality | Comment
-----|-------|-------------|--------
dcat:byteSize | rdfs:Literal typed as xsd:decimal | 0..1 | This property contains the size of a Distribution in bytes.
dcat:downloadURL | rdfs:Resource | 0..n | This property contains a URL that is a direct link to a downloadable file in a given format.
dct:conformsTo | dct:Standard | 0..n | This property refers to an established schema to which the described Distribution conforms.
dct:issued | rdfs:Literal typed as xsd:date or xsd:dateTime | 0..1 | This property contains the date of formal issuance (e.g., publication) of the Distribution.
dct:rights | dct:RightsStatement | 0..1 | This property refers to a statement that specifies rights associated with the Distribution.
dcat:spatialResolutionInMeters | xsd:decimal | 0..n | This property refers to the  minimum spatial separation resolvable in a dataset distribution, measured in meters.
adms:status | skos:Concept | 0..1 | This property refers to the maturity of the Distribution. It MUST take one of the values Completed, Deprecated, Under Development, Withdrawn.
dcat:temporalResolution | xsd:duration | 0..n | This property refers to the minimum time period resolvable in the dataset distribution.
**dct:temporal** | dct:PeriodOfTime | 0..n | This property refers to a temporal period that the Distribution covers.
dct:title | rdfs:Literal | 0..n | This property contains a name given to the Distribution. This property can be repeated for parallel language versions of the description.
dct:modified | rdfs:Literal typed as xsd:date or xsd:dateTime | 0..1 | This property contains the most recent date on which the Distribution was changed or modified.
dcatap:applicableLegislation | hvd:LegalResource | 0..n | The legislation that mandates the creation or management of the Dataset.
 

 
 
