# Generated by Django 5.0.1 on 2024-02-10 01:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("item", "0003_itemstockinfo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="itemstockinfo",
            name="item",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="item_stock_info",
                to="item.item",
            ),
        ),
    ]
