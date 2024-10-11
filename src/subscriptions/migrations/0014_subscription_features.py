# Generated by Django 5.0.9 on 2024-10-11 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("subscriptions", "0013_subscription_featured_subscription_order_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="subscription",
            name="features",
            field=models.TextField(
                blank=True,
                help_text="Features for pricing, separated by new line",
                null=True,
            ),
        ),
    ]