# Generated by Django 5.0.1 on 2024-02-09 20:54

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0005_remove_phonecharge_amount_remove_phonecharge_status_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="phonecharge",
            name="tracking_code",
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
