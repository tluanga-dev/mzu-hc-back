# Generated by Django 5.0.1 on 2024-05-10 05:41

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("patient", "0003_remove_patient_age_remove_patient_created_on_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="patient",
            old_name="student_id",
            new_name="mzu_student_id",
        ),
        migrations.RemoveField(
            model_name="patient",
            name="mzu_user",
        ),
    ]