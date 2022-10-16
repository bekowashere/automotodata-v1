"""
/auto : BrandListSerializer - BrandListAPIView
/auto/<brand_slug> : BrandDetailSerializer - BrandDetailAPIView
/auto/<brand_slug>/<series_slug> : SeriesDetailSerializer - SeriesDetailAPIView

/auto/<brand_slug>/<series_slug>/<model_slug> : ModelDetailSerializer
/cars/<car_slug> : CarDetailSerializer
"""
from django.urls import path
from auto.api.views import (
    BrandListAPIView,
    BrandDetailAPIView,
    SeriesDetailAPIView,
    ModelDetailAPIView,
    CarDetailAPIView
)

app_name = 'auto'

urlpatterns = [
    path('auto/', BrandListAPIView.as_view(), name='brand_list'),
    path('auto/<brand_slug>', BrandDetailAPIView.as_view(), name='brand_detail'),
    path('auto/<brand_slug>/<series_slug>', SeriesDetailAPIView.as_view(), name='series_detail'),
    path('auto/<brand_slug>/<series_slug>/<model_slug>', ModelDetailAPIView.as_view(), name='model_detail'),
    path('cars/<car_slug>', CarDetailAPIView.as_view(), name='car_detail'),

]