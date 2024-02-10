# Generated by Django 5.0.1 on 2024-02-07 00:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("item", "0002_alter_itembatch_item"),
    ]

    operations = [
        migrations.CreateModel(
            name="ItemStockInfo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
                ("quantity", models.PositiveIntegerField()),
                ("remarks", models.CharField(blank=True, max_length=200, null=True)),
                (
                    "item",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="item_stock_info",
                        to="item.item",
                    ),
                ),
            ],
        ),
    ]