# Generated by Django 5.0.1 on 2024-05-21 03:13

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="IdManager",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("prefix", models.CharField(max_length=255, unique=True)),
                ("latest_id", models.TextField()),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
