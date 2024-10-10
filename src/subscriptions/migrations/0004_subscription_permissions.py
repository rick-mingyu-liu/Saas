# Generated by Django 5.0.9 on 2024-10-10 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("subscriptions", "0003_subscription_groups"),
    ]

    operations = [
        migrations.AddField(
            model_name="subscription",
            name="permissions",
            field=models.ManyToManyField(to="auth.permission"),
        ),
    ]
