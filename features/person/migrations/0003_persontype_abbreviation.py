# Generated by Django 5.0.1 on 2024-04-04 16:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("person", "0002_remove_person_department"),
    ]

    operations = [
        migrations.AddField(
            model_name="persontype",
            name="abbreviation",
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]