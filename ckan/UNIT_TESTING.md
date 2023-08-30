# Running unit tests in Docker

## Environment setup

**1. Add test instance of Solr to your docker-compose.override.yml**

```yaml
solr-test:
  image: registrydata/solr:latest
  build:
    context: ./solr
  expose:
    - 8983
  networks:
    - backend
  volumes:
    - solr_test_data:/opt/solr/server/solr/ckan/data
  restart: unless-stopped
```

**2. Add configuration to ckanext/ckan/test-core.ini**

```ini
[app:main]
use = config:../../src/ckan/test-core.ini
sqlalchemy.url = postgresql://ckan:ckan_pass@postgres/ckan_test
solr_url = http://solr-test:8983/solr/ckan
ckan.redis.url = redis://redis:6379/1
```

**3. Start the solr-test container**
`docker-compose -p registrydata up -d solr-test`

**4. Start a shell in ckan-container**
`docker exec -it registrydata-ckan-1 bash`

**5. Run pytest**
```bash
cd ckanext/ckanext-registrydata
pytest
```

## Troubleshooting

### Database not found
The test database is created in `ckan/scripts/init_ckan.sh` so it happens only once. Drop the container and associated volumes and redeploy them.