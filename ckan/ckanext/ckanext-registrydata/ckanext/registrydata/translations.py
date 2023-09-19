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

    # search results
    _('{number} dataset found for "{query}"')
    _('{number} datasets found for "{query}"')
    _('No datasets found for "{query}"')
    _('{number} dataset found')
    _('{number} datasets found')
    _('No datasets found')

    # login
    _('Username or Email')
