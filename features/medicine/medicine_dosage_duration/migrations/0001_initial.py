# Generated by Django 5.0.1 on 2024-01-23 07:14

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("medicine_dosage", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="MedicineDosageDuration",
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
                ("days", models.IntegerField()),
                ("name", models.CharField(max_length=255)),
                ("updated_on", models.DateTimeField(auto_now=True)),
                (
                    "medicine_dosage",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="durations",
                        to="medicine_dosage.medicinedosage",
                    ),
                ),
            ],
        ),
    ]