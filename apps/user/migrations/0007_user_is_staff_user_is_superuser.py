# Generated by Django 4.2.8 on 2024-09-14 13:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0006_remove_user_is_staff_remove_user_is_superuser"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="is_staff",
            field=models.BooleanField(default=False, verbose_name="Staff"),
        ),
        migrations.AddField(
            model_name="user",
            name="is_superuser",
            field=models.BooleanField(default=False, verbose_name="Superuser"),
        ),
    ]
