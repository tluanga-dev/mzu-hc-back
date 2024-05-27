# Generated by Django 5.0.1 on 2024-05-26 15:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("inventory_transaction", "0001_initial"),
        ("supplier", "__first__"),
    ]

    operations = [
        migrations.CreateModel(
            name="IndentInventoryTransaction",
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
                ("supply_order_no", models.CharField(max_length=250, unique=True)),
                ("supply_order_date", models.DateField()),
                ("date_of_delivery", models.DateField()),
                (
                    "supplier",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="supplier.supplier",
                    ),
                ),
            ],
            bases=("inventory_transaction.inventorytransaction",),
        ),
    ]
