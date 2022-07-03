![django-test](https://github.com/alfabalf/donunay/actions/workflows/django-test.yaml/badge.svg) [![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-310/)
    

## dolunay

### Run It

Run docker-compose for supporting services:
- localstack for local s3 endpoint
- postgres

```bash
docker-compose -f docker-compose-dev.yaml up --force-recreate --renew-anon-volumes
```

#### Run tests
```bash
python manage.py test
```

### Run API
```bash
python manage.py migrate
python manage.py loaddata initial_data.json
python manage.py runserver
```

Access admin panel at http://localhost:8000/admin
 - username: test@test.com
 - password: password

### Example API Usage:

```bash
NEW_ALBUM_ID=$(curl -F \
  data="{\"name\": \"First Album\", \"description\": \"good times\", \"start_date\": \"1981-01-01\", \"end_date\": \"1981-12-01\" }" \
  -F file=@api/restapp/tests/resources/sample_album_cover.jpg \
  http://localhost:8000/api/album | jq '.id' --raw-output)

curl http://localhost:8000/api/album/$NEW_ALBUM_ID | jq
{
  "id": 1,
  "name": "First Album",
  "description": "good times",
  "cover_image_key": "album/b4c4f307-3ca7-4080-8ecc-912d6385964f",
  "start_date": "1981-01-01",
  "end_date": "1981-12-01"
}
```

