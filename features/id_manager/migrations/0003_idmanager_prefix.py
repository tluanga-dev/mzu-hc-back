# Generated by Django 5.0.1 on 2024-01-24 07:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("id_manager", "0002_alter_idmanager_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="idmanager",
            name="prefix",
            field=models.CharField(default=1, max_length=255, unique=True),
            preserve_default=False,
        ),
    ]
