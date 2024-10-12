from typing import Any
from django.core.management.base import BaseCommand, CommandParser
from subscriptions import utils as sub_utils
import helpers.billing
class Command(BaseCommand):
    
    def add_arguments(self, parser):
        parser.add_argument("--clear-dangling", action="store_true", default=False)
    
    def handle(self, *args: Any, **options: Any):
        # python manage.py sync_users_subs --clear-dangling
        clear_dangling = options.get("clear_dangling")
        if clear_dangling:
            print("clear dangling not in use active subs in stripe")
            sub_utils.clear_dangling_subs()
        else:
            print("sync active subs")
            print("Done")
            
            