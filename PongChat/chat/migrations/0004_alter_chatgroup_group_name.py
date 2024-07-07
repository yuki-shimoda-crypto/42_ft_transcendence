# Generated by Django 5.0.4 on 2024-06-16 08:06

import shortuuid.main
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0003_alter_chatgroup_group_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="chatgroup",
            name="group_name",
            field=models.CharField(
                default=shortuuid.main.ShortUUID.uuid, max_length=128, unique=True
            ),
        ),
    ]
