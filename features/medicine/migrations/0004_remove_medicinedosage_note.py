# Generated by Django 5.0.1 on 2024-04-25 08:11

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        (
            "medicine",
            "0003_rename_daymedschedule_medicinedosagetiming_day_med_schedule_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="medicinedosage",
            name="note",
        ),
    ]