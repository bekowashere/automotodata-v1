from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.utils.crypto import get_random_string
from django.utils.text import slugify

# MODELS
from account.models import User, CustomerUser
from subscribe.models import Plan, Subscription

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'email', 'first_name', 'last_name', 'is_active', 'is_customer'
        )

class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        # return str(token)
        return str(token.access_token)

    class Meta:
        model = User
        fields = (
            'id', 'email', 'first_name', 'last_name', 'is_active', 'is_customer', 'token'
        )

# CUSTOMER REGISTER
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = [
            'membership_type'
        ]
        extra_kwargs = {
            'membership_type': {'read_only': True}
        }

class CustomerUserRegisterSerializer(serializers.ModelSerializer):
    """
    {
        "email": "beko@gmail.com",
        "password": "Berke1919",
        "password2": "Berke1919",
        "is_active": true,
        "is_customer": true,
        "customer": {}
    }
    """
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    token = serializers.SerializerMethodField(read_only=True)
    customer = CustomerSerializer(read_only=True)

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'password',
            'password2',
            'is_active',
            'is_customer',
            'customer',
            'token'
        )
        extra_kwargs = {
            'username': {'read_only': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        email = validated_data['email']
        _username = email.split('@')[0]

        ex = False
        ex = User.objects.filter(username=_username).exists()
        while ex:
            _username = f'{_username}-{get_random_string(9, "0123456789")}'
            ex = User.objects.filter(username=_username).exists()

        # User
        user = User.objects.create(
            username=_username,
            email=email,
            is_active=True,
            is_customer=True,
        )
        user.set_password(validated_data['password'])
        user.save()

        # Customer
        CustomerUser.objects.create(user=user)
        return user