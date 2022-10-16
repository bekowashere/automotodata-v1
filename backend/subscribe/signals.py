from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from subscribe.models import Plan, Subscription
from account.models import User, CustomerUser

import datetime
from datetime import timedelta
today = datetime.date.today()

@receiver(post_save, sender=Subscription)
def create_subscription(sender, instance, created, **kwargs):
    if created:
        instance.expiry_date = instance.start_date + timedelta(days=instance.period_duration)
        instance.save()
    else:
        """
        FREE = 'F'
        BRONZE = 'B'
        SILVER = 'S'
        GOLD = 'G'
        DIAMOND = 'D'
        """
        customer = instance.user

        if instance.plan.slug == "free-trial":
            customer.membership_type = 'F'
            customer.save()
        elif instance.plan.slug == "bronze":
            customer.membership_type = 'B'
            customer.save()
        elif instance.plan.slug == "silver":
            customer.membership_type = 'S'
            customer.save()
        elif instance.plan.slug == "gold":
            customer.membership_type = 'G'
            customer.save()
        elif instance.plan.slug == "diamond":
            customer.membership_type = 'D'
            customer.save()


# @receiver(post_save, sender=Subscription)
# def update_activate(sender, instance, created, **kwargs):
#     if instance.expiry_date < today:
#         instance.is_active = False
#         instance.save()
#     else:
#         instance.is_active= True
#         instance.save()