from django.contrib import admin
from subscribe.models import Plan, Subscription
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Plan Information'), {'fields': ('name', 'slug', 'show_total_subscription')}),
        (_('Requests'), {'fields': ('daily_request',)}),
        (_('Price'), {'fields': ('price',)})
    )
    list_display = ('name', 'slug', 'daily_request', 'price', 'show_total_subscription')
    search_fields = ('name', 'slug')
    ordering = ('price',)
    readonly_fields = ('show_total_subscription',)

    # property fieldını da readonly_fields içerisine ekleyerek adminde gösterebiliriz
    def show_total_subscription(self, obj):
        result = Subscription.objects.filter(plan=obj).count()
        format = format_html("<b>{}</b>", result)
        return format

    show_total_subscription.short_description = _("Subscriptions")

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Subscription Information'), {'fields': ('user', 'plan', 'is_active')}),
        (_('Period'), {'fields': ('period_type', 'period_duration')}),
        (_('Subscription Date'), {'fields': ('start_date', 'expiry_date')}),
        (_('Price'), {'fields': ('paid_amount', 'show_plan_price')}),
    )
    list_display = ('user', 'plan', 'period_type', 'start_date', 'expiry_date', 'is_active')
    list_filter = ('period_type', 'is_active')
    search_fields = ('user__user__email', 'plan__name')
    ordering = ('start_date',)
    readonly_fields = ('show_plan_price',)

    def show_plan_price(self, obj):
        all_plans = Plan.objects.all()
        plan_text = ""
        for plan in all_plans:
            plan_text += f'{plan.name} - {plan.price}\n'

        return plan_text

    show_plan_price.short_description = _("Plan Price")
