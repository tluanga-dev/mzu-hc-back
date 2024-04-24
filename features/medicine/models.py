import uuid
from django.db import models
from features.base.time_stamped_abstract_class import TimeStampedAbstractModelClass

from features.item.models import Item

class MedicineDosage(TimeStampedAbstractModelClass):
    DURATION_CHOICES = [
        ('days', 'Days'),
        ('weeks', 'Weeks'),
        ('months', 'Months'),
        ('next_visit', 'Until Next Visit'),
        ('other', 'Other'),
    ]
    medicine = models.ForeignKey(
        Item, 
        related_name='medicine_dosage', 
        on_delete=models.CASCADE
    )
    duration_value=models.IntegerField(blank=True, null=True)
    duration_type = models.CharField(max_length=10, choices=DURATION_CHOICES, default='days')
    note=models.TextField(null=True, blank=True)

class MedicineDosageTiming(TimeStampedAbstractModelClass):
    quantity_in_one_take = models.IntegerField()
    # dayMedSchedule can have values like-morning, afternoon, evening,noon
    day_med_schedule = models.CharField(max_length=255)
    # medicineTiming can have values like- before meal, after meal,
    # before lunch, after lunch, before bed 
    medicine_timing = models.CharField(max_length=255)
    medicine_dosage = models.ForeignKey(MedicineDosage,  on_delete=models.CASCADE, related_name='medicine_dosage_timing_set')

    class Meta:
        app_label = 'medicine'
