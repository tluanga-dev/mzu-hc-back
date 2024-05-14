# Generated by Django 5.0.1 on 2024-05-14 17:10

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Supplier",
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
                ("name", models.CharField(max_length=255)),
                ("abbreviation", models.CharField(max_length=255)),
                ("contact_no", models.PositiveBigIntegerField(blank=True, null=True)),
                ("email", models.EmailField(blank=True, max_length=255, null=True)),
                ("address", models.TextField(blank=True, null=True)),
                ("remarks", models.TextField(blank=True, null=True)),
            ],
        ),
    ]
