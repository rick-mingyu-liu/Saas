from subscriptions.models import UserSubscription, Subscription
import helpers.billing
from customers.models import Customer

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