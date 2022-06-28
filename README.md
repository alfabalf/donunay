![django-test](https://github.com/alfabalf/donunay/actions/workflows/django-test.yaml/badge.svg) [![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-310/)
    

## dolunay

### Make It Go

```bash
docker-compose up -d
export LOCALSTACK_ENDPOINT_URL=http://localhost:4566
aws --endpoint-url=$LOCALSTACK_ENDPOINT_URL s3 mb s3://dolunay-storage
docker-compose exec web python manage.py migrate
 docker-compose exec web python manage.py loaddata initial_data.json
```

Goto: http://localhost:8000/

### Run Tests
```bash
docker-compose -f docker-compose-dev.yaml up -d 
export LOCALSTACK_ENDPOINT_URL=http://localhost:4566
aws --endpoint-url=$LOCALSTACK_ENDPOINT_URL s3 mb s3://dolunay-storage
cd api
python manage.py test
```
