# Generated by Django 5.0.1 on 2024-04-04 21:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("person", "0003_persontype_abbreviation"),
    ]

    operations = [
        migrations.AlterField(
            model_name="person",
            name="email",
            field=models.EmailField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]