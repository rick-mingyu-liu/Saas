from typing import Any
from django.core.management.base import BaseCommand

from subscriptions.models import Subscription

class Command(BaseCommand):
    
    def handle(self, *args: Any, **options: Any):
        # print("hello world")
        qs = Subscription.objects.filter(active=True)
        for obj in qs:
            sub_perms = obj.permissions.all()
            for group in obj.groups.all():
                for per in obj.permissions.all():
                    group.permissions.set(sub_perms)