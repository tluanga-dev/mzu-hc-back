# Generated by Django 5.0.1 on 2024-02-04 22:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("item_batch", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="itembatch",
            name="date_of_expiry",
            field=models.DateField(),
        ),
    ]
