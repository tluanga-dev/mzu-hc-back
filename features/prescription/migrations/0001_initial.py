# Generated by Django 5.0.1 on 2024-06-01 00:54

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("item", "0001_initial"),
        ("medicine", "0001_initial"),
        ("patient", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Prescription",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("code", models.CharField(blank=True, max_length=255, unique=True)),
                ("chief_complaints", models.TextField()),
                ("diagnosis", models.TextField()),
                ("advice_and_instructions", models.TextField()),
                ("note", models.TextField()),
                ("date_and_time", models.DateTimeField()),
                (
                    "prescription_dispense_status",
                    models.CharField(
                        choices=[
                            ("dispensed", "Dispensed"),
                            ("not_dispensed", "Not Dispensed"),
                        ],
                        default="not_dispensed",
                        max_length=100,
                    ),
                ),
                (
                    "patient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="prescriptions_patient",
                        to="patient.patient",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="PrescriptionItem",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("note", models.TextField(blank=True, null=True)),
                (
                    "dosages",
                    models.ManyToManyField(
                        related_name="dosages", to="medicine.medicinedosage"
                    ),
                ),
                (
                    "medicine",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="medicine_items",
                        to="item.item",
                    ),
                ),
                (
                    "prescription",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="prescribed_item_set",
                        to="prescription.prescription",
                    ),
                ),
            ],
        ),
    ]
