# Generated by Django 5.0.1 on 2024-06-24 01:12

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ItemCategory",
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
                ("name", models.CharField(max_length=255, unique=True)),
                ("abbreviation", models.CharField(max_length=4)),
                ("description", models.TextField()),
            ],
            options={
                "indexes": [
                    models.Index(fields=["name"], name="itemcategory_name_idx")
                ],
            },
        ),
        migrations.CreateModel(
            name="ItemPackaging",
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
                ("name", models.CharField(max_length=255)),
                ("label", models.CharField(max_length=255, unique=True)),
                ("unit", models.CharField(max_length=255)),
            ],
            options={
                "indexes": [models.Index(fields=["label"], name="packaging_label_idx")],
            },
        ),
        migrations.CreateModel(
            name="ItemType",
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
                ("name", models.CharField(max_length=255, unique=True)),
                ("abbreviation", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("example", models.TextField()),
                (
                    "category",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="item.itemcategory",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MedicineDosageUnit",
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
                ("name", models.CharField(max_length=255, unique=True)),
                ("description", models.TextField()),
                ("example", models.TextField()),
                ("dosage_example", models.TextField()),
            ],
            options={
                "indexes": [models.Index(fields=["name"], name="dosageunit_name_idx")],
            },
        ),
        migrations.CreateModel(
            name="UnitOfMeasurement",
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
                ("name", models.CharField(max_length=255)),
                ("abbreviation", models.CharField(max_length=255, unique=True)),
                ("description", models.TextField()),
                ("example", models.TextField()),
            ],
            options={
                "indexes": [
                    models.Index(fields=["abbreviation"], name="uom_abbreviation_idx")
                ],
            },
        ),
        migrations.CreateModel(
            name="Item",
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
                ("name", models.CharField(max_length=255, unique=True)),
                ("contents", models.TextField(blank=True, null=True)),
                ("item_code", models.CharField(max_length=255, unique=True)),
                ("description", models.TextField()),
                ("is_consumable", models.BooleanField(default=False)),
                (
                    "packaging",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="item.itempackaging",
                    ),
                ),
                (
                    "type",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="item.itemtype",
                    ),
                ),
                (
                    "medicine_dosage_unit",
                    models.ManyToManyField(
                        related_name="medicine_dosage_unit",
                        to="item.medicinedosageunit",
                    ),
                ),
                (
                    "unit_of_measurement",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="item.unitofmeasurement",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ItemBatch",
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
                ("batch_id", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, null=True)),
                ("date_of_expiry", models.DateField()),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="item_batches",
                        to="item.item",
                    ),
                ),
            ],
            options={
                "indexes": [
                    models.Index(fields=["batch_id"], name="itembatch_batch_id_idx")
                ],
            },
        ),
        migrations.AddIndex(
            model_name="itemtype",
            index=models.Index(fields=["name"], name="itemtype_name_idx"),
        ),
        migrations.AddIndex(
            model_name="item",
            index=models.Index(fields=["name"], name="item_name_idx"),
        ),
        migrations.AddIndex(
            model_name="item",
            index=models.Index(fields=["item_code"], name="item_code_idx"),
        ),
    ]
