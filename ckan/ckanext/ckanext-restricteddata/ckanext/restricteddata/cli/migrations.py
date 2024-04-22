import ckan.plugins.toolkit as toolkit
from .migrate import apply_patches, package_generator
get_action = toolkit.get_action


#
# Migrations
#

def migrations():
    return [('1.4.1', '1.5.0', migrate_1_4_1_to_1_5_0),
            ]


#
# Migration step functions
#

def no_changes(*args, **kwargs):
    pass


def migrate_1_4_1_to_1_5_0(ctx, config, dryrun, echo=print):
    from ckanext.restricteddata.dcat import FREQUENCY_MAP
    package_patches = [{'id': package['id'], 'update_frequency': None}
                       for package in package_generator()
                       if package.get('update_frequency') not in FREQUENCY_MAP]
    apply_patches(package_patches=package_patches, dryrun=dryrun, echo=echo)
