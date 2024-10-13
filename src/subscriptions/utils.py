from subscriptions.models import UserSubscription, Subscription, SubscriptionStatus
import helpers.billing
from django.db.models import Q
from customers.models import Customer

def refresh_active_users_subscriptions(user_ids=None, 
                                       active_only=True, 
                                       days_ago=-1,
                                       days_left=-1,
                                       day_start=-1,
                                       day_end=-1
                                       ):
    qs = UserSubscription.objects.all()
    if active_only:
        qs = qs.by_active_trialing()
    if user_ids is not None:
        qs = qs.by_user_ids(user_ids=user_ids)
    if days_ago > -1:
        qs = qs.by_days_ago(days_ago=days_ago)
    if days_left > -1:
        qs = qs.by_days_left(days_ago=days_ago)
    if day_start > -1 and day_end > -1:
        qs = qs.by_range(day_start=day_start, days_end=day_end)
        
    complete_count = 0
    qs_count = qs.count()
    active_qs = qs.filter(status=SubscriptionStatus.ACTIVE)
    trialing_qs = qs.filter(status=SubscriptionStatus.TRIALING)
    qs = (active_qs | trialing_qs)
    for obj in qs: 
        if obj.stripe_id:
            sub_data = helpers.billing.cancel_subscription(
                obj.stripe_id, 
                reason="User wanted to end", 
                feedback="other",
                cancel_at_period_end=True,
                raw=False
            )
            for k,v in sub_data.items():
                setattr(obj, k, v)
            obj.save()
            complete_count += 1
    return complete_count == qs_count

def clear_dangling_subs():
    qs = Customer.objects.filter(stripe_id__isnull=False)
    for customer_obj in qs:
        user = customer_obj.user
        customer_stripe_id = customer_obj.stripe_id
        print("Sync {user} - {customer_stripe_id} subs and remove old ones")
        subs = helpers.billing.get_customer_active_subscriptions(customer_stripe_id)
        for sub in subs:
            existing_user_sub_qs = UserSubscription.objects.filter(stripe_id__iexact=f"{sub.id}".strip())
            if existing_user_sub_qs.exists():
                continue
            helpers.billing.cancel_subscription(sub.id, 
                                                reason="Dangling active subscription", 
                                                cancel_at_period_end=False
                                                )
            print(sub.id, existing_user_sub_qs.exists())
            
            
def sync_subs_groups_permissions():
    qs = Subscription.objects.filter(active=True)
    for obj in qs:
        sub_perms = obj.permissions.all()
        for group in obj.groups.all():
            for per in obj.permissions.all():
                group.permissions.set(sub_perms)