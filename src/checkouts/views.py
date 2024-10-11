from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from subscriptions.models import SubscriptionPrice
from django.urls import reverse
from django.conf import settings
import helpers.billing

BASE_URL = settings.BASE_URL
# Create your views here.
def product_price_redirect_view(request, price_id=None, *args, **kwargs):
    request.session["checkout_subscription_price_id"] = price_id
    return redirect("/checkout")


@login_required
def checkout_redirect_view(request):
    checkout_subscription_price_id = request.session.get("checkout_subscription_price_id")
    try:
        obj = SubscriptionPrice.objects.get(id=checkout_subscription_price_id)
    except:
        obj = None
    if checkout_subscription_price_id is None or obj is None:
        return redirect("pricing")
    customer_stripe_id = request.user.customer.stripe_id
    success_url_path = reverse("stripe-checkout-end")
    pricing_url_path = reverse("pricing")
    cancel_url = f"{BASE_URL}{pricing_url_path}"
    success_url = f"{BASE_URL}{success_url_path}"
    price_stripe_id = obj.stripe_id
    url = helpers.billing.start_checkout_session(
        customer_stripe_id,
        success_url=success_url,
        cancel_url=cancel_url,
        price_stripe_id=price_stripe_id,
        raw=False
    )
    return redirect(url)

def checkout_finalize_view(request):
    session_id = request.GET.get("session_id")
    checkout_r = helpers.billing.get_checkout_session(session_id, raw=True)
    customer_id = checkout_r.customer
    sub_stripe_id = checkout_r.subscription
    sub_r = helpers.billing.get_subscription(sub_stripe_id, raw=True)
    sub_plan = sub_r.plan
    sub_plan_price_stripe_id = sub_plan.id
    price_qs  = SubscriptionPrice.objects.filter(strip_id=sub_plan_price_stripe_id)
    print(price_qs)
    context = {
        "subscription": sub_r,
        "checkout": checkout_r  
    }
    return render(request, "checkout/success.html")