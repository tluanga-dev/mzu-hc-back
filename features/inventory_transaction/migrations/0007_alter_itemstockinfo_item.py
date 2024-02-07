# Generated by Django 5.0.1 on 2024-02-07 00:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("inventory_transaction", "0006_itemstockinfo"),
        ("item", "0002_alter_itembatch_item"),
    ]

    operations = [
        migrations.AlterField(
            model_name="itemstockinfo",
            name="item",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="item_stock_info",
                to="item.item",
            ),
        ),
    ]
