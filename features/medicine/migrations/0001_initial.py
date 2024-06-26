# Generated by Django 5.0.1 on 2024-02-17 10:43

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("item", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="MedicineDosage",
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
                ("quantity_in_one_take", models.IntegerField()),
                ("how_many_times_in_a_day", models.IntegerField()),
                ("name", models.CharField(max_length=255)),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="dosages",
                        to="item.item",
                    ),
                ),
            ],
        ),
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
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("days", models.IntegerField()),
                ("name", models.CharField(max_length=255)),
                (
                    "medicine_dosage",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="medicine.medicinedosage",
                    ),
                ),
            ],
        ),
    ]
