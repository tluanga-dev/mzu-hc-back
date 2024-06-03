# Generated by Django 5.0.1 on 2024-06-03 10:40

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("person", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Patient",
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
                (
                    "mzu_hc_id",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                (
                    "patient_type",
                    models.CharField(
                        choices=[
                            ("Employee", "Employee"),
                            ("Employee Dependent", "Employee Dependent"),
                            ("Student", "Student"),
                            ("MZU Outsider", "MZU Outsider"),
                        ],
                        max_length=255,
                    ),
                ),
                ("illness", models.JSONField(blank=True, default=list, null=True)),
                ("allergy", models.JSONField(blank=True, default=list, null=True)),
                (
                    "employee",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="person.employee",
                    ),
                ),
                (
                    "employee_dependent",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="person.employeedependent",
                    ),
                ),
                (
                    "mzu_outsider",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="person.mzuoutsider",
                    ),
                ),
                (
                    "student",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="person.student",
                    ),
                ),
            ],
            options={
                "verbose_name": "Patient",
                "verbose_name_plural": "Patients",
                "ordering": ["-created_at"],
                "indexes": [
                    models.Index(
                        fields=["mzu_hc_id"], name="patient_pat_mzu_hc__d844c3_idx"
                    ),
                    models.Index(
                        fields=["patient_type"], name="patient_pat_patient_629fc5_idx"
                    ),
                ],
            },
        ),
        migrations.AddConstraint(
            model_name="patient",
            constraint=models.UniqueConstraint(
                fields=("employee", "student", "employee_dependent", "mzu_outsider"),
                name="unique_patient",
            ),
        ),
    ]
