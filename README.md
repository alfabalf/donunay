### dolunay

### Dump and Load initial data
python manage.py dumpdata --format=json restapp > initial_data.json
python manage.py loaddata initial_data.json 
