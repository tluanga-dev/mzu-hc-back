# Generated by Django 5.0.1 on 2024-02-04 17:31

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        (
            "inventory_transaction",
            "0003_alter_inventorytransaction_inventory_transaction_id",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="inventorytransaction",
            name="status",
        ),
    ]