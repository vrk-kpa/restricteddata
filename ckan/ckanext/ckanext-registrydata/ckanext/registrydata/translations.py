# -*- coding: utf-8 -*-

def _translations():
    """ Does nothing but hints message extractor to extract missing strings. """
    from ckan.common import _

    # ckanext_pages
    _("eg. Page Title")
    _("URL")
    _("Publish Date")
    _("Header Order")
    _("Not in Menu")
    _("Are you sure you want to delete this Page?")

    # search
    _('Relevance')

    # login
    _('Username or Email')

    # Translations for keys from schema
    _("fi")
    _("en")
    _("sv")

    # Dataset
    _("Dataset title")
    _("* Required field")
    _("e.g. Finnish names")
    _("Give a short and descriptive name for the dataset.<br><br>The URL is created automatically based on the dataset title. You can edit the URL if you want.")  # noqa: E501
    _("Dataset description")
    _("Write a description for the dataset.")
    _("Describe the dataset’s contents, collection process, quality and  possible limits, flaws and applications in a comprehensible way. Use as confining terms as possible to make it easier to find and understand the data.")  # noqa: E501
    _("Keywords and categories")
    _("Keywords help users to find your data. Select at least one keyword in Finnish and Swedish.")  # noqa: E501
    _("Select at least one category.")
    _("Dataset additional information")
    _("Select a license that suits your needs. We recommend using CC0 or CC BY 4 -licenses.")
    _("Collection type")
    _("Restricted")
    _("Non-public")
    _("Rights")
    _("High value dataset")
    _("You can mark dataset as high value dataset")
    _("Yes")
    _("No")
    _("Links to additional information")
    _("Add links to one or more websites with additional information about the data.")
    _("e.g. www.dvv.fi")
    _("Add link")
    _("Update frequency")
    _("Describe how often your data is updated")
    _("e.g. monthly")
    _("Valid from")
    _("Valid till")
    _("Dataset producer and maintainer")
    _("Select the dataset publisher (organisation).")
    _("Dataset maintainer")
    _("e.g. Digital and Population Data Services Agency")
    _("The dataset maintainer will receive updates about the dataset to the email address specified in this form. We recommend using a general email address instead of the contact information of a single employee. Note that the dataset information can only be managed by registered users with Editor- or Admin-rights in the publishing organisation.")  # noqa: E501
    _("Maintainer email")
    _("e.g. rekisteridata@dvv.fi")
    _("Maintainer website")
    _("e.g. www.rekisteridata.fi")
    _("The data license you select above only applies to the contents of any resource files that you add to this dataset. By submitting this form, you agree to release the metadata values that you enter into the form under the Open Database License.")  # noqa: E501
    _('You can set the state of the dataset back to active.')
    _('Deleted. The dataset is only visible to logged in users of the producer organization.')
    _('In draft state. The dataset is only visible to logged in users of the producer organization.')
    _('Private mode. The dataset is only visible to logged in users of the producer organization.')

    # Resource
    _("Data resource title")
    _("Write a short and descriptive name for the data resource. If the data covers a specific time frame, mention that in the name.")  # noqa: E501
    _("e.g. Most popular Finnish first names 2019")
    _("Resource *")
    _("Add the data resource by adding a link to the data.")  # noqa: E501
    _("Data")
    _("Resource URL")
    _("Size")
    _("Data resource description")
    _("Write a description for the resource")
    _("Describe the data clearly and concisely. Use as confining terms as possible to make it easier to find and understand the data.")  # noqa: E501
    _("Additional information")
    _("Write a rights statement for the resource")
    _("Endpoint URL")
    _("Distribution visibility")
    _("You can set the visibility to private temporarily for example if the distribution is missing some information. Private distributions are visible to all members of the producer-organisation.")  # noqa: E501
    _("Data status")
    _("Define a state for the data. This is recommended especially if your dataset has data resources from multiple years.")
    _("Current version")
    _("Draft version")
    _("Archived version")
    _("Coordinate system")
    _("If your data includes geographic information, specify the coordinate system it uses.")
    _("e.g. WGS84 (World Geodetic System 1984)")
    _("Select the time frame by which the data is separated. For example, does the resource include data from every week or month.")  # noqa: E501
    _("Temporal granularity")
    _("e.g. a month")
    _("Time Frame")
    _("Start date")
    _("End date")
    _("Geographical accuracy")
    _("If your data includes geographic information, specify the accuracy in meters")
