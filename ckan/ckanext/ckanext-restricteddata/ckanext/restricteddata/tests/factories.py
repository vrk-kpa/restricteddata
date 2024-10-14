import factory

from ckan.tests.factories import Organization

from faker import Faker

fake = Faker()

class RestrictedDataOrganization(Organization):
    title_translated = factory.Dict({
        'fi': factory.LazyFunction(lambda: fake.sentence(nb_words=5)),
        'sv': factory.LazyFunction(lambda: fake.sentence(nb_words=5))
    })
