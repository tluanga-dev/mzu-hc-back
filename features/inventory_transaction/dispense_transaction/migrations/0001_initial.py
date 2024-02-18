# Generated by Django 5.0.1 on 2024-02-18 08:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("inventory_transaction", "0001_initial"),
        ("prescription", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="DispenseInventoryTransaction",
            fields=[
                (
                    "inventorytransaction_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="inventory_transaction.inventorytransaction",
                    ),
                ),
                ("dispense_date", models.DateField()),
                (
                    "prescription",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="dispened_prescription",
                        to="prescription.prescription",
                    ),
                ),
            ],
            bases=("inventory_transaction.inventorytransaction",),
        ),
    ]
