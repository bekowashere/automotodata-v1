### START GUIDE

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate

pyhton manage.py createsuperuser
```

### SUBSCRIBE

```
python manage.py add_plans
```


### AUTO

(add_brands is enough for test phrase)
```
python manage.py add_brands


python manage.py add_series
python manage.py add_models
python manage.py add_specification_types
python manage.py add_specifications
python manage.py add_cars
```

### CLEAR PYCACHE - MIGRATIONS

```
clear.sh
```