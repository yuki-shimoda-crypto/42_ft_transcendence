# Generated by Django 5.0.4 on 2024-06-17 07:28

import shortuuid.main
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0005_chatgroup_blocked_users_alter_chatgroup_group_name"),
    ]

    operations = [
        migrations.RenameField(
            model_name="chatgroup",
            old_name="blocked_users",
            new_name="user_bloks",
        ),
        migrations.AlterField(
            model_name="chatgroup",
            name="group_name",
            field=models.CharField(
                default=shortuuid.main.ShortUUID.uuid, max_length=128, unique=True
            ),
        ),
    ]