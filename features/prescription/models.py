import uuid
from django.db import models

from features.base.time_stamped_abstract_class import TimeStampedAbstractModelClass
from features.id_manager.models import IdManager
from features.item.models import Item
from features.medicine.models import MedicineDosage
from features.person.models import Person
from django.db import transaction

PRESCRIPTION_ABBREVIATION = 'PRESC'
class Prescription(TimeStampedAbstractModelClass):
    
    class PresciptionDispenseStatus(models.TextChoices):
        DISPENSED = 'dispensed', 'Dispensed'
        NOT_DISPENSED = 'not_dispensed', 'Not Dispensed'
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code=models.CharField(max_length=255,unique=True)
    patient = models.ForeignKey(Person, related_name='prescriptions_patient', on_delete=models.CASCADE)
    doctor = models.ForeignKey(Person, related_name='prescriptions_doctor', on_delete=models.CASCADE)
    chief_complaints=models.TextField()
    diagnosis = models.TextField()
    advice_and_instructions=models.TextField()
    note= models.TextField()
    date_and_time = models.DateTimeField()
    prescription_dispense_status = models.CharField(
        max_length=100, 
        choices=PresciptionDispenseStatus.choices, 
        default=PresciptionDispenseStatus.NOT_DISPENSED
        
    )

    def get_prescribed_medicine_by_patient(self, patient_id):
        return self.prescribed_medicine_set.filter(prescription__patient_id=patient_id)
    
    def save(self, *args, **kwargs):
        self.code = IdManager.generateId(prefix=PRESCRIPTION_ABBREVIATION)
        super().save(*args, **kwargs)


class PrescriptionItem(TimeStampedAbstractModelClass):
    name = models.CharField(max_length=255)
    dosages = models.ManyToManyField(MedicineDosage, related_name='dosages')
    item = models.ForeignKey(
        Item, 
        related_name='medicine_items', 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL
    )
    prescription = models.ForeignKey(
        Prescription, 
        related_name='prescribed_item_set'
        ,on_delete=models.CASCADE
    )

    class Meta:
        app_label = "prescription"


    