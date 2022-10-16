from django.urls import path
from account.api.views import (
    # CUSTOMER
    CustomerUserRegisterAPIView
)

app_name = 'account'

urlpatterns = [
    # CUSTOMER
    path('register/customer/', CustomerUserRegisterAPIView.as_view(), name='customer_register'),
]
