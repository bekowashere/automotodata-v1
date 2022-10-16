"""
/auto : BrandListSerializer
/auto/<brand_slug> : BrandDetailSerializer
/auto/<brand_slug>/<series_slug> : SeriesDetailSerializer
/auto/<brand_slug>/<series_slug>/<model_slug> : ModelDetailSerializer
/cars/<car_slug> : CarDetailSerializer
"""
# Cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers

# Rest Framework Helpers
from rest_framework.response import Response
from rest_framework import status

# Rest Framework Views
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView
)

from auto.models import Brand, Series, Model, Car

from auto.api.serializers import (
    BrandListSerializer,
    BrandDetailSerializer,
    SeriesDetailSerializer,
    ModelDetailSerializer,
    CarDetailSerializer
)
from rest_framework.permissions import IsAuthenticated
from account.throttling import SubscriptionDailyRateThrottle

# ! /auto : BrandListSerializer - BrandListAPIView
class BrandListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [SubscriptionDailyRateThrottle]

    queryset = Brand.objects.all()
    serializer_class = BrandListSerializer

    # With cookie: cache requested url for each user for 1 minute
    @method_decorator(cache_page(60*1))
    @method_decorator(vary_on_cookie)
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

# ! /auto/<brand_slug> : BrandDetailSerializer - BrandDetailAPIView
class BrandDetailAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [SubscriptionDailyRateThrottle]

    queryset = Brand.objects.all()
    serializer_class = BrandDetailSerializer
    lookup_field = 'brand_slug'

    # With cookie: cache requested url for each user for 2 hours
    @method_decorator(cache_page(60*1))
    @method_decorator(vary_on_cookie)
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

# ! /auto/<brand_slug>/<series_slug> : SeriesDetailSerializer - SeriesDetailAPIView
class SeriesDetailAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [SubscriptionDailyRateThrottle]

    queryset = Series.objects.all()
    serializer_class = SeriesDetailSerializer

    # With cookie: cache requested url for each user for 2 hours
    @method_decorator(cache_page(60*1))
    @method_decorator(vary_on_cookie)
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    def get_object(self):
        brand_slug = self.kwargs.get('brand_slug')
        series_slug = self.kwargs.get('series_slug')
        brand = Brand.objects.get(brand_slug=brand_slug)
        return Series.objects.get(series_brand=brand, series_slug=series_slug)

# ! /auto/<brand_slug>/<series_slug>/<model_slug> : ModelDetailSerializer - ModelDetailAPIView
class ModelDetailAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [SubscriptionDailyRateThrottle]

    queryset = Model.objects.all()
    serializer_class = ModelDetailSerializer

    # With cookie: cache requested url for each user for 2 hours
    @method_decorator(cache_page(60*1))
    @method_decorator(vary_on_cookie)
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    def get_object(self):
        brand_slug = self.kwargs.get('brand_slug')
        series_slug = self.kwargs.get('series_slug')
        model_slug = self.kwargs.get('model_slug')

        brand = Brand.objects.get(brand_slug=brand_slug)
        series = Series.objects.get(series_slug=series_slug)
        return Model.objects.get(model_brand=brand, model_series=series, model_slug=model_slug)

# ! /cars/<car_slug> : CarDetailSerializer - CarDetailAPIView
class CarDetailAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [SubscriptionDailyRateThrottle]
    
    queryset = Car.objects.all()
    serializer_class = CarDetailSerializer
    lookup_field = 'car_slug'

    # With cookie: cache requested url for each user for 2 hours
    @method_decorator(cache_page(60*1))
    @method_decorator(vary_on_cookie)
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)