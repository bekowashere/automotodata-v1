from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from account.models import User, CustomerUser
from account.forms import CustomUserCreationForm
from subscribe.models import Subscription

@admin.register(User)
class MyUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    fieldsets = (
        (_('Login Information'), {'fields': ('email', 'username', 'password')}),
        (_('Personal Information'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser', 'is_customer', 'groups', 'user_permissions'
            )
        }),
        (_('Dates'), {'fields': ('last_login', 'date_joined')}),
    )

    # ADD USER FIELD
    add_fieldsets = (
        (_('Login Information'), {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )

    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('date_joined',)
    filter_horizontal = (
        'groups',
        'user_permissions',
    )

class SubscriptionInline(admin.StackedInline):
    model = Subscription


@admin.register(CustomerUser)
class CustomerUserAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('User'), {'fields': ('user',)}),
        (_('Membership Type'), {'fields': ('membership_type',)}),
    )

    list_display = ('user', 'membership_type')
    list_filter = ('membership_type',)
    search_fields = ('user__email__icontains',)

    inlines = [SubscriptionInline]