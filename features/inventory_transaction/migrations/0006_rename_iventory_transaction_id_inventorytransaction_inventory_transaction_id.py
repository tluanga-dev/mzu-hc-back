# Generated by Django 5.0.1 on 2024-01-27 21:18

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        (
            "inventory_transaction",
            "0005_remove_indentinventorytransaction_quantity_and_more",
        ),
    ]

    operations = [
        migrations.RenameField(
            model_name="inventorytransaction",
            old_name="iventory_transaction_id",
            new_name="inventory_transaction_id",
        ),
    ]
