from rest_framework.throttling import  UserRateThrottle
from account.models import User, CustomerUser


def get_user_daily_limit(user):
    """
    plan_daily_request = None > Plan is Diamond (unlimited requests)
    """
    customer = CustomerUser.objects.get(user=user)
    subscription = customer.user_subscription
    plan = subscription.plan
    plan_daily_request = plan.daily_request

    return plan_daily_request

class SubscriptionDailyRateThrottle(UserRateThrottle):
    scope = "subscription"

    def __init__(self):
        super().__init__()

    def allow_request(self, request, view):
        if request.user.is_authenticated:
            user_daily_limit = get_user_daily_limit(request.user)
            if user_daily_limit:
                # Override the default from settings.py
                """
                # day = 86400
                # hour = 3600
                # minute = 60
                # second = 1
                duration = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}
                """
                self.duration = 86400
                self.num_requests = user_daily_limit
            else:
                # No limit == unlimited plan
                return True


        # Parent method logical
        if self.rate is None:
            return True

        self.key = self.get_cache_key(request, view)
        if self.key is None:
            return True

        self.history = self.cache.get(self.key, [])
        self.now = self.timer()

        # Drop any requests from the history which have now passed the
        # throttle duration
        while self.history and self.history[-1] <= self.now - self.duration:
            self.history.pop()
        if len(self.history) >= self.num_requests:
            return self.throttle_failure()
        return self.throttle_success()