# Generated by Django 5.0.1 on 2024-04-24 21:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("item", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="contents",
            field=models.TextField(blank=True, null=True),
        ),
    ]
