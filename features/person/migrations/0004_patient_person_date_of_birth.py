# Generated by Django 5.0.1 on 2024-04-25 04:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("person", "0003_alter_person_department"),
    ]

    operations = [
        migrations.CreateModel(
            name="Patient",
            fields=[
                (
                    "person_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="person.person",
                    ),
                ),
                ("illness", models.JSONField(blank=True, default=list, null=True)),
                ("allergy", models.JSONField(blank=True, default=list, null=True)),
            ],
            bases=("person.person",),
        ),
        migrations.AddField(
            model_name="person",
            name="date_of_birth",
            field=models.DateField(blank=True, null=True),
        ),
    ]
