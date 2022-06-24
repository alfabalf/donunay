## dolunay

### Dump and Load initial data
python manage.py dumpdata --format=json restapp > initial_data.json
python manage.py loaddata initial_data.json 

### Run postgres in docker container

Intellij instructions are same for PyCharm. 
https://www.jetbrains.com/help/idea/running-a-dbms-image.html

Environment Variables: POSTGRES_HOST_AUTH_METHOD=trust; POSTGRES_DB=dolunay

### Run Docker, Load Init Data, Start App

See `./run` for configuration details.

The main Django Server run configuration needs 3 'before launch' run configurations to be run first
1. the docker run configuration
2. configuration to run `python manage.py migrate`
3. configuration to run `python manage.py loaddata initial_data.json`

