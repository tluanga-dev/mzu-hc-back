# Generated by Django 5.0.1 on 2024-05-20 10:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("inventory_transaction", "0001_initial"),
        ("organisation_unit", "__first__"),
    ]

    operations = [
        migrations.CreateModel(
            name="IssueItemInventoryTransaction",
            fields=[
                (
                    "inventorytransaction_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="inventory_transaction.inventorytransaction",
                    ),
                ),
                ("issue_date", models.DateField()),
                ("item_receiver", models.CharField(max_length=200)),
                (
                    "issue_to",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="issue_to",
                        to="organisation_unit.organisationunit",
                    ),
                ),
            ],
            bases=("inventory_transaction.inventorytransaction",),
        ),
    ]
