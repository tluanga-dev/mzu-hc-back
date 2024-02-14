from django.db import models

from features.base.time_stamped_abstract_class import TimeStampedAbstractModelClass
from features.item.models import Item


class Prescription(TimeStampedAbstractModelClass):
    class PressciptionDispenseStatus(models.TextChoices):
        DISPENSED = 'dispensed', 'Dispensed'
        NOT_DISPENSED = 'not_dispensed', 'Not Dispensed'
    patient_name = models.CharField(max_length=255)
    doctor_name = models.CharField(max_length=255)
    note= models.TextField()
    prescription_date = models.DateField()
    prescription_dispense_status = models.CharField(
        max_length=100, 
        choices=PressciptionDispenseStatus.choices, 
        default=PressciptionDispenseStatus.NOT_DISPENSED
        
    )
    class Meta:
        app_label = "prescription"


class PrescribedMedicine(TimeStampedAbstractModelClass):
    name = models.CharField(max_length=255)
    dosage = models.TextField()
    item = models.ForeignKey(
        Item, 
        related_name='medicine_items', 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL
    )
    prescription = models.ForeignKey(
        Prescription, 
        related_name='prescribed_medicines'
        ,on_delete=models.CASCADE
    )

    class Meta:
        app_label = "prescription"


    