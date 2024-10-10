from django.db import models
from django.contrib.auth.models import Group, Permission


SUBSCRIPTION_PERMISSION = [
            ("advanced", "Advanced Perm"),# subscriptions.advanced
            ("pro", "Pro Perm"), # subscriptions.pro
            ("basic", "Basic Perm"), # subscriptions.basic
            ("basic_ai", "Basic AI Perm"), # subscriptions.basic_ai
        ]


# Create your models here.
class Subscription(models.Model):
    name = models.CharField(max_length=120)
    groups = models.ManyToManyField(Group)
    permissions =  models.ManyToManyField(Permission, limit_choices_to={
        "content_type__app_label": "subscriptions", 
        "codename__in": [x[0] for x in SUBSCRIPTION_PERMISSION]}
    ) 
    
    class Meta:
        permissions = SUBSCRIPTION_PERMISSION