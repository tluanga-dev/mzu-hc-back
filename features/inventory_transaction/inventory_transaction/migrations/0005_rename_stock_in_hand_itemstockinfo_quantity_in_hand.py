# Generated by Django 5.0.1 on 2024-05-01 09:30

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("inventory_transaction", "0004_itemstockinfo_stock_in_hand"),
    ]

    operations = [
        migrations.RenameField(
            model_name="itemstockinfo",
            old_name="stock_in_hand",
            new_name="quantity_in_hand",
        ),
    ]