# Generated by Django 4.2.8 on 2024-09-14 13:17

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0002_remove_user_user_role_user_role"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="fcm_token",
        ),
        migrations.RemoveField(
            model_name="user",
            name="is_staff",
        ),
        migrations.RemoveField(
            model_name="user",
            name="is_superuser",
        ),
    ]
