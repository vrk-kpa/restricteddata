import jwt
import datetime
from ckan.plugins import toolkit

def minimal_dataset(user):
    return dict(
        user=user,
        private=False,
        title_translated={'fi': 'Title (fi)', 'sv': 'Title (sv)'},
        notes_translated={'fi': 'Notes (fi)', 'sv': 'Notes (sv)'},
        access_rights='non-public',
        maintainer='maintainer',
        maintainer_email=['maintainer@example.com'],
        keywords={'fi': ['test-fi'], 'sv': ['test-sv']},
    )


def minimal_dataset_with_one_resource_fields(user):
    dataset = minimal_dataset(user)
    dataset['resources'] = [dict(
            url='http://example.com',
            format='TXT',
            size=1234,
            rights_translated={'fi': 'Rights (fi)', 'sv': 'Rights (sv)'},
            private=False,
            maturity='current',
        )]
    return dataset


def minimal_group():
    return dict(
        title_translated={lang: f'title {lang}' for lang in ['fi', 'sv']}
    )


def create_paha_token(data):
    payload = {
        "iss": "PAHA",
        "expiresIn": int((datetime.datetime.now() + datetime.timedelta(days=1)).timestamp() * 1000),
    }
    payload.update(data)
    key = toolkit.config['ckanext.restricteddata.paha_jwt_key']
    algorithm = toolkit.config['ckanext.restricteddata.paha_jwt_algorithm']
    token = jwt.encode(payload, key, algorithm=algorithm)
    return token
