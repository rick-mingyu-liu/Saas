# Generated by Django 5.0.9 on 2024-10-12 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("subscriptions", "0016_usersubscription_stripe_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="usersubscription",
            name="user_cancel",
            field=models.BooleanField(default=False),
        ),
    ]
