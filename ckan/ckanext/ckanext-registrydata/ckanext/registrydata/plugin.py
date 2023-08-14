import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckanext.pages.interfaces import IPagesSchema

import logging


log = logging.getLogger(__name__)

class RegistrydataPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, "templates")
        toolkit.add_public_directory(config_, "public")
        toolkit.add_resource("assets", "registrydata")


class RegistrydataPagesPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(IPagesSchema)

    def update_config(self, config_):
        log.info("REGISTRYDATA_PAGES update_config")
        toolkit.add_template_directory(config_, "templates_pages")

    # IPagesSchema
    def update_pages_schema(self, schema):
        log.info("REGISTRYDATA_PAGES update_pages_schema")
        schema.update({
            'title_fi': [],
            'title_sv': [],
            'title_en': [],
            'content_fi': [],
            'content_sv': [],
            'content_en': [],
            'submenu_order': []
            })
        return schema
