# Generated by Django 5.0.1 on 2024-01-26 18:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "inventory_transaction",
            "0003_remove_indentinventorytransaction_requested_quantity_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="inventorytransaction",
            name="remarks",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]