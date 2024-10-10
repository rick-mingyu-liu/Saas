from django.db import models
from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_save
from django.conf import settings


User = settings.AUTH_USER_MODEL # auth user 

SUBSCRIPTION_PERMISSION = [
            ("advanced", "Advanced Perm"),# subscriptions.advanced
            ("pro", "Pro Perm"), # subscriptions.pro
            ("basic", "Basic Perm"), # subscriptions.basic
            ("basic_ai", "Basic AI Perm"), # subscriptions.basic_ai
        ]


# Create your models here.
class Subscription(models.Model):
    name = models.CharField(max_length=120)
    active = models.BooleanField(default=True)
    groups = models.ManyToManyField(Group) # one to one
    permissions =  models.ManyToManyField(Permission, limit_choices_to={
        "content_type__app_label": "subscriptions", 
        "codename__in": [x[0] for x in SUBSCRIPTION_PERMISSION]}
    ) 
    
    def __str__(self):
        return f"{self.name}"
    
    
    class Meta:
        permissions = SUBSCRIPTION_PERMISSION
        
class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True)
    active = models.BooleanField(default=True)


def user_sub_post_save(sender, instance, *args, **kwargs):
    user_sub_instance = instance
    user = user_sub_instance.user
    subscription_obj = user_sub_instance.subscription
    groups = subscription_obj.groups.all()
    user.groups.set(groups)
    
post_save.connect(user_sub_post_save, sender=UserSubscription)