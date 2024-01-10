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
    _("Give a short and descriptive name for the dataset.<br><br>The URL is created automatically based on the dataset title. If necessary, you can edit the URL.")  # noqa: E501
    _("Dataset description")
    _("Write a description for the dataset.")
    _("Describe the dataset’s contents, collection process, quality of the data and possible limits, flaws and applications in an easily understandable way.")  # noqa: E501
    _("Keywords and categories")
    _("Select at least one keyword relating to your data that helps users to find your data.")  # noqa: E501
    _("Select at least one category.")
    _("Dataset additional information")
    _("Select a license that suits your needs.")
    _("Collection type")
    _("Restricted")
    _("Non-public")
    _("Rights")
    _("High value dataset")
    _("You can mark dataset as high value dataset")
    _("Select access rights for your dataset:<br><br><b>Non-public</b> datasets may include resources that contain sensitive or personal information.<br><br><b>Restricted</b> datasets may include resources that require payment, resources shared under non-disclosure agreements, resources for which the publisher or owner has not yet decided if they can be publicly released.")  # noqa: E501
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
    _("There is no description for this dataset")
    _("Dataset visibility")
    _("false")
    _("true")
    _("Access rights")
    _("More about access rights")
    _("active")
    _("e.g. names")
    _("Dataset publisher and maintainer")
    _("Publisher")
    _("You're currently viewing an old version of this dataset. Data files may not match the old version of the metadata. <a href=\"%(url)s\">View the current version</a>.")  # noqa: E501
    _("View changes from")
    _("to")
    _("Show metadata diff")

    # Resource
    _("Data resource title")
    _("Give a short and descriptive name for the distribution. If the data covers a specific time frame, mention that in the name.")  # noqa: E501
    _("e.g. Most popular Finnish first names 2019")
    _("Resource *")
    _("Add the distribution by adding a link to the data.")  # noqa: E501
    _("Data")
    _("Resource URL")
    _("Select a file format for the distribution")
    _("Size")
    _("Data resource description")
    _("Write a description for the resource")
    _("Describe the data clearly and concisely. Use as confining terms as possible to make it easier to find and understand the data.")  # noqa: E501
    _("Describe terms and conditions for re-use. Include how to apply for use permit and information about possible payments and their principles.")  # noqa: E501
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
    _("Metadata last updated")
    _("Conditions for re-use")
    _("Resources")
    _("Unnamed resource")
    _("Add view")
    _("All views")
    _("View view")
    _("eg. My View")
    _("eg. Information about my view")
    _("Image url")
    _("eg. http://example.com/image.jpg (if blank uses resource url)")

    # Organization
    _("Groups")
    _("Formats")
    _("Organization name")
    _("Organization description")
    _("Common, compact and plain description about the organization")
    _("Other information")
    _("View Organization")

    # Dashboard
    _("News feed")
    _("Activity from items that I'm following")
    _("My Datasets")
    _("Add Dataset")
    _("My Organizations")
    _("Add Group")
    _("My Groups")

    # Activity streams
    _("Activity type")
    _("All activity types")
    _("Newer activities")
    _("Older activities")
    _("{actor} created the group {group}")
    _("{actor} updated the group {group}")
    _("{actor} deleted the group {group}")
    _("{actor} created the organization {organization}")
    _("{actor} updated the organization {organization}")
    _("{actor} deleted the organization {organization}")
    _("{actor} created the {dataset_type} {dataset}")
    _("{actor} updated the {dataset_type} {dataset}")
    _("{actor} deleted the {dataset_type} {dataset}")
    _("{actor} added the resource {resource} to the dataset {dataset}")
    _("{actor} updated the resource {resource} in the dataset {dataset}")
    _("{actor} deleted the resource {resource} from the dataset {dataset}")
    _("{actor} {activity_type}")
    _("{actor} added the tag {tag} to the dataset {dataset}")
    _("{actor} removed the tag {tag} from the dataset {dataset}")
    _("{actor} updated their profile")
    _("{actor} started following {dataset}")
    _("{actor} started following {group}")
    _("{actor} started following {user}")
    _("new package")
    _("changed package")
    _("deleted package")
    _("follow dataset")

    # Humanize translations
    _("Add {object_type}")
    _("Create {object_type}")
    _("View {object_type}")
    _("Edit {object_type}")
    _("Save {object_type}")
    _("Search {object_type}s...")
    _("Update {object_type}")
    _("A little information about my {object_type}...")
    _("There are no {object_type}s associated with this dataset")
    _("There are currently no {object_type}s for this site")
    _("There is no description for this {object_type}")
    _("You are not a member of any {object_type}s.")
    _("{object_type} Form")
    _("My {object_type}s")
    _("My {object_type}")
    _("No {object_type}")
    _("{object_type}s")

