# Generated by Django 5.0.4 on 2024-06-15 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_customuser_is_remote_multiplayer_active_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="last_active",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
