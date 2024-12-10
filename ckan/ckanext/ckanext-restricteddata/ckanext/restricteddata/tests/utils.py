import jwt
import datetime
from pathlib import Path
from ckan.plugins import toolkit

def minimal_dataset(user):
    return dict(
        user=user,
        private=False,
        title_translated={'fi': 'Title (fi)'},
        notes_translated={'fi': 'Notes (fi)'},
        access_rights='non-public',
        maintainer='maintainer',
        maintainer_email=['maintainer@example.com'],
        keywords={'fi': ['test-fi']},
    )


def minimal_dataset_with_one_resource_fields(user):
    dataset = minimal_dataset(user)
    dataset['resources'] = [dict(
            url='http://example.com',
            format='TXT',
            size=1234,
            rights_translated={'fi': 'Rights (fi)'},
            private=False,
            maturity='current',
        )]
    return dataset


def minimal_group():
    return dict(
        title_translated={lang: f'title {lang}' for lang in ['fi']}
    )


def create_paha_token(data, private_key_file='jwtRS256.valid.key'):
    payload = {
        "iss": "PAHA",
        "id": "user-id",
        "email": "foo.bar@example.com",
        "firstName": "Foo",
        "lastName": "Bar",
        "activeOrganizationId": "organization-id",
        "activeOrganizationNameFi": "organization name fi",
        "activeOrganizationNameSv": "organization name sv",
        "activeOrganizationNameEn": "organization name en",
        "expiresIn": int((datetime.datetime.now() + datetime.timedelta(days=1)).timestamp() * 1000),
    }
    payload.update(data)
    private_key = (Path(__file__).parent / 'data' / private_key_file).open().read()
    algorithm = toolkit.config['ckanext.restricteddata.paha_jwt_algorithm']
    token = jwt.encode(payload, private_key, algorithm=algorithm)
    return token

def get_auth_token_for_paha_token(app, paha_token):
    client = app.test_client()
    response = client.post(toolkit.url_for('paha.authorize'), data=paha_token)
    return response
