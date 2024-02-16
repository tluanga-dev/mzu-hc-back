from django.db import models

from features.base.time_stamped_abstract_class import TimeStampedAbstractModelClass
from features.id_manager.models import IdManager
from features.item.models import Item
from features.person.models import Person

PRESCRIPTION_ABBREVIATION = 'PRESC'
class Prescription(TimeStampedAbstractModelClass):
    class PressciptionDispenseStatus(models.TextChoices):
        DISPENSED = 'dispensed', 'Dispensed'
        NOT_DISPENSED = 'not_dispensed', 'Not Dispensed'
    code=models.CharField(max_length=255,unique=True)
    patient = models.ForeignKey(Person, related_name='prescriptions_patient', on_delete=models.CASCADE)
    doctor = models.ForeignKey(Person, related_name='prescriptions_doctor', on_delete=models.CASCADE)
    note= models.TextField()
    prescription_date = models.DateTimeField()
    prescription_dispense_status = models.CharField(
        max_length=100, 
        choices=PressciptionDispenseStatus.choices, 
        default=PressciptionDispenseStatus.NOT_DISPENSED
        
    )

    def get_prescribed_medicine_by_patient(self, patient_id):
        return self.prescribed_medicine_set.filter(prescription__patient_id=patient_id)

    def save(self, *args, **kwargs):
        if not self.code:
            
            generated_item_code = IdManager.generateId(PRESCRIPTION_ABBREVIATION)
            # print(generated_item_code)
            self.code = generated_item_code

        super().save(*args, **kwargs)
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
        related_name='prescribed_medicine_set'
        ,on_delete=models.CASCADE
    )

    class Meta:
        app_label = "prescription"


    