# Generated by Django 5.0.9 on 2024-10-11 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("subscriptions", "0015_subscription_subtitle"),
    ]

    operations = [
        migrations.AddField(
            model_name="usersubscription",
            name="stripe_id",
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]