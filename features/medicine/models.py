import uuid
from django.db import models
from features.base.time_stamped_abstract_class import TimeStampedAbstractModelClass

from features.item.models import Item
class MedicineQuantityInOneTakeUnit(TimeStampedAbstractModelClass):
    item=models.ManyToManyField(Item, related_name='medicine_quantity_in_one_take_unit')
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        app_label = 'medicine'


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
    note=models.TextField(blank=True, null=True)

class MedicineDosageTiming(TimeStampedAbstractModelClass):
    quantity_in_one_take = models.IntegerField()
    quantity_in_one_take_unit = models.ManyToManyField(MedicineQuantityInOneTakeUnit)
    # dayMedSchedule can have values like-morning, afternoon, evening,noon
    day_med_schedule = models.CharField(max_length=255)
    # medicineTiming can have values like- before meal, after meal,
    # before lunch, after lunch, before bed 
    medicine_timing = models.CharField(max_length=255)
    medicine_dosage = models.ForeignKey(MedicineDosage,  on_delete=models.CASCADE, related_name='medicine_dosage_timing_set')

    class Meta:
        app_label = 'medicine'
