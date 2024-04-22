def minimal_dataset_with_one_resource_fields(user):
    return dict(
        user=user,
        private=False,
        title_translated={'fi': 'Title (fi)', 'sv': 'Title (sv)'},
        notes_translated={'fi': 'Notes (fi)', 'sv': 'Notes (sv)'},
        access_rights='non-public',
        maintainer='maintainer',
        maintainer_email=['maintainer@example.com'],
        keywords={'fi': ['test-fi'], 'sv': ['test-sv']},
        resources=[dict(
            url='http://example.com',
            format='TXT',
            size=1234,
            rights_translated={'fi': 'Rights (fi)', 'sv': 'Rights (sv)'},
            private=False,
            maturity='current',
        )]
    )


