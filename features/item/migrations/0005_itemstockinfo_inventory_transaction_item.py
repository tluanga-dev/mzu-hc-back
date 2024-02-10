# Generated by Django 5.0.1 on 2024-02-10 01:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "inventory_transaction",
            "0010_remove_inventorytransactionitem_item_stock_info",
        ),
        ("item", "0004_alter_itemstockinfo_item"),
    ]

    operations = [
        migrations.AddField(
            model_name="itemstockinfo",
            name="inventory_transaction_item",
            field=models.OneToOneField(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="item_stock_info",
                to="inventory_transaction.inventorytransactionitem",
            ),
            preserve_default=False,
        ),
    ]
