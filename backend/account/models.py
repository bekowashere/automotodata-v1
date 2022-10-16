from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone

from django.utils.translation import gettext_lazy as _
# from django.contrib.auth import get_user_model

class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with given email and password
        """

        if not email:
            raise ValueError(_('You must provide an email address'))

        if not password:
            raise ValueError(_('User must have a password'))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        user = self._create_user(email, password=password, **extra_fields)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True'))

        user = self._create_user(email, password=password, **extra_fields)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('Username'),
        max_length=128,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(
        _('Email Address'),
        unique=True,
        help_text=_('Required. 50 characters or fewer. Example: john.doe@gmail.com'),
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )

    first_name = models.CharField(_('First Name'), max_length=64, blank=True)
    last_name = models.CharField(_('Last Name'), max_length=64, blank=True)

    is_active = models.BooleanField(_('Active'), default=True)
    is_staff = models.BooleanField(_('Staff User'), default=False)
    is_superuser = models.BooleanField(_('Superuser'), default=False)

    date_joined = models.DateTimeField(default=timezone.now, editable=False)
    last_login = models.DateTimeField(auto_now=True)

    #
    is_customer = models.BooleanField(_('Customer'), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.get_username()

    def get_full_name(self):
        """
        Return the first_name + last_name
        """
        full_name = f'{self.first_name} {self.last_name}'
        return full_name

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

# ! CUSTOMER
class CustomerUser(models.Model):
    FREE = 'F'
    BRONZE = 'B'
    SILVER = 'S'
    GOLD = 'G'
    DIAMOND = 'D'

    MEMBERSHIPS = [
        (FREE, 'Free'),
        (BRONZE, 'Bronze Member'),
        (SILVER, 'Silver Member'),
        (GOLD, 'Gold Member'),
        (DIAMOND, 'Diamond Member'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name=_('User'),
        related_name='customer'
    )

    membership_type = models.CharField(
        _('Membership Type'),
        max_length=1,
        choices=MEMBERSHIPS,
        default=FREE
    )


    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')