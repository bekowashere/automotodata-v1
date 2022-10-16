
from django.db import models
from django.utils.translation import gettext_lazy as _
from account.models import User, CustomerUser

from datetime import datetime as dt

class Plan(models.Model):
    name = models.CharField(_('Plan Name'), max_length=48)
    slug = models.SlugField(_('Plan Slug'), unique=True)
    daily_request = models.IntegerField(_('Daily Request Limit'), blank=True, null=True)
    price = models.DecimalField(
        _('Price'),
        max_digits=9,
        decimal_places=2
    )

    def __str__(self):
        return self.name

    @property
    def total_subscriptions(self):
        return self.plan_subscriptions.all().count()

    class Meta:
        verbose_name = _('Plan')
        verbose_name_plural = _('Plans')

class Subscription(models.Model):
    PERIOD_TYPE = (
        (0, 'Monthly'),
        (1, 'Yearly')
    )
    user = models.OneToOneField(
        CustomerUser,
        on_delete=models.CASCADE,
        related_name="user_subscription",
        verbose_name=_('User')
    )
    plan = models.ForeignKey(
        Plan,
        on_delete=models.CASCADE,
        related_name="plan_subscriptions",
        verbose_name=_('Plan')
    )

    period_type = models.IntegerField(choices=PERIOD_TYPE, default=0)
    period_duration = models.PositiveIntegerField(default=30)

    # Django Warning = start_date, use django.utils.timezone.now
    start_date = models.DateField(default=dt.now().date())
    expiry_date = models.DateField(
        _('Expiry Date'),
        blank=True,
        null=True
        # default=dt.now().date() + timedelta(days=period_duration)
    )

    paid_amount = models.DecimalField(
        _('Paid Amount'),
        max_digits=9,
        decimal_places=2
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user.user.email} - {self.plan.name}'

    class Meta:
        verbose_name = _('Subscription')
        verbose_name_plural = _('Subscriptions')