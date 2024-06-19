# Generated by Django 5.0.4 on 2024-06-17 08:38

import shortuuid.main
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0006_rename_blocked_users_chatgroup_user_bloks_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="chatgroup",
            name="user_bloks",
        ),
        migrations.AlterField(
            model_name="chatgroup",
            name="group_name",
            field=models.CharField(
                default=shortuuid.main.ShortUUID.uuid, max_length=128, unique=True
            ),
        ),
    ]