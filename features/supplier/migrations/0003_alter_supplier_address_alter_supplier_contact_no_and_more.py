# Generated by Django 5.0.1 on 2024-02-18 17:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("supplier", "0002_supplier_abbreviation"),
    ]

    operations = [
        migrations.AlterField(
            model_name="supplier",
            name="address",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="supplier",
            name="contact_no",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="supplier",
            name="email",
            field=models.EmailField(blank=True, max_length=255, null=True),
        ),
    ]
