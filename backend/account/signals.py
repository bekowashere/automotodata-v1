from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from subscribe.models import Plan, Subscription
from account.models import User, CustomerUser

@receiver(post_save, sender=CustomerUser)
def create_customer_user(sender, instance, created, *args, **kwargs):
    if created:
        free_plan = Plan.objects.get(slug="free-trial")
        subscription = Subscription(
            user=instance,
            plan=free_plan,
            paid_amount=free_plan.price
        )
        subscription.save()
