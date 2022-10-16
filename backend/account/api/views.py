# REST FRAMEWORK
from rest_framework.response import Response
from rest_framework import status

# REST FRAMEWORK VIEWS
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView

# REST FRAMEWORK - JWT
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

# PERMISSIONS
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

# HELPERS
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from rest_framework.parsers import FileUploadParser
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

# MODELS
from account.models import User, CustomerUser

# SERIALIZERS
from account.api.serializers import (
    UserSerializerWithToken,
    CustomerUserRegisterSerializer
)

# ! USER LOGIN
class MyTokenObtainPairSerializer(TokenObtainSerializer):
    def validate(self, attrs):
        data = super(MyTokenObtainPairSerializer, self).validate(attrs)

        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# V1 Register
class CustomerUserRegisterAPIView(APIView):
    serializer_class = CustomerUserRegisterSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'user': serializer.data}, status=status.HTTP_200_OK)
        return Response({'status': 'error', 'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
