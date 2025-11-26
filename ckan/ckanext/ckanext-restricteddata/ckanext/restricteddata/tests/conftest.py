import pytest


@pytest.fixture
def clean_db(reset_db, migrate_db_for):
    reset_db()
    migrate_db_for("restricteddata")
    migrate_db_for("activity")  # https://github.com/ckan/ckan/issues/8540
