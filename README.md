# START GUIDE

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

# ENDPOINTS

### ACCOUNT


:heavy_check_mark: **[POST]** `api/token/` - *MyTokenObtainPairView*

:heavy_check_mark: **[POST]** `api/account/register/customer/` - *CustomerUserRegisterAPIView*


### AUTO


:heavy_check_mark: **[GET]** `api/auto/` - *BrandListAPIView*

:heavy_check_mark: **[GET]** `api/auto/<brand_slug>` - *BrandDetailAPIView*

:heavy_check_mark: **[GET]** `api/auto/<brand_slug>/<series_slug>` - *SeriesDetailAPIView*

:heavy_check_mark: **[GET]** `api/auto/<brand_slug>/<series_slug>/<model_slug>` - *ModelDetailAPIView*

:heavy_check_mark: **[GET]** `api/cars/<car_slug>` - *CarDetailAPIView*