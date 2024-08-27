import pytest

from ckanext.restricteddata import model
from ckan.model import meta


@pytest.fixture
def restricteddata_setup():
    model.init_db(meta.engine)
