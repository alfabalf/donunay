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
  json="{\"name\": \"My Album\", \"description\": \"good times\"}" \
  -F file=@api/restapp/tests/resources/album_cover.jpeg \
  http://localhost:8000/api/album | jq '.uuid' --raw-output)

curl http://localhost:8000/api/album/$NEW_ALBUM_ID | jq
{
  "uuid": "1b99834a-0c6e-4880-9300-01a275d4b955",
  "name": "My Album",
  "description": "good times",
  "cover_image_key": "album/1b99834a-0c6e-4880-9300-01a275d4b955"
}

```

