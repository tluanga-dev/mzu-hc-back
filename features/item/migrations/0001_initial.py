# Generated by Django 5.0.1 on 2024-04-19 04:59

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
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
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("name", models.CharField(max_length=255)),
                ("item_code", models.CharField(max_length=255, unique=True)),
                ("description", models.TextField()),
                ("is_consumable", models.BooleanField(default=False)),
            ],
        ),
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
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("name", models.CharField(max_length=255)),
                ("abbreviation", models.CharField(max_length=4)),
                ("description", models.TextField()),
            ],
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
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("name", models.CharField(max_length=255)),
                ("abbreviation", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("example", models.TextField()),
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
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
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
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("name", models.CharField(max_length=255)),
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
        migrations.AddField(
            model_name="item",
            name="type",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="item.itemtype",
            ),
        ),
        migrations.AddField(
            model_name="item",
            name="unit_of_measurement",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="item.unitofmeasurement"
            ),
        ),
    ]
