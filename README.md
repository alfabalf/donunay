![django-test](https://github.com/alfabalf/donunay/actions/workflows/django-test.yaml/badge.svg) [![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-310/)
    

## dolunay

### Run it

Start app and postgres containers in docker-compose, and migrate db
```bash
docker-compose up
docker-compose exec web python manage.py migrate
```

Goto: http://localhost:8000/

To load intial data (contains superuser: test@test.com/password)
```bash
 docker-compose exec web python manage.py loaddata initial_data.json
```

