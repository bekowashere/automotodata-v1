from django.core.management import BaseCommand, CommandError
from subscribe.models import Plan
import json

class Command(BaseCommand):
    def handle(self, *args, **options):
        file_path = '_data/subscribe/all_plans.json'

        with open(file_path, 'r', encoding="UTF-8") as f:
            data = json.load(f)

        for plan in data:
            plan_name = plan['name']
            plan_slug = plan['slug']
            plan_daily_request = plan['daily_request']
            plan_price = plan['price']

            try:
                plan = Plan(
                    name=plan_name,
                    slug=plan_slug,
                    daily_request=plan_daily_request,
                    price=plan_price
                )
                plan.save()
                self.stdout.write(self.style.SUCCESS(f'{plan_name} create successfully'))
            except Exception as e:
                raise CommandError(f'{e}')