# Generated by Django 5.0.1 on 2024-02-05 07:55

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("inventory_transaction", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="indentinventorytransaction",
            old_name="date_of_delivery",
            new_name="date_of_deliverty",
        ),
        migrations.RenameField(
            model_name="indentinventorytransaction",
            old_name="supply_order_date",
            new_name="supply_order_date",
        ),
        migrations.RenameField(
            model_name="indentinventorytransaction",
            old_name="supplyOrderNo",
            new_name="supply_order_no",
        ),
    ]