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
    note= models.TextField()
    date_and_time = models.DateTimeField()
    prescription_dispense_status = models.CharField(
        max_length=100, 
        choices=PresciptionDispenseStatus.choices, 
        default=PresciptionDispenseStatus.NOT_DISPENSED
        
    )

    def get_prescribed_medicine_by_patient(self, patient_id):
        return self.prescribed_medicine_set.filter(prescription__patient_id=patient_id)
    

    @classmethod
    @transaction.atomic
    def create_full_prescription(cls, prescription_data, prescription_item_data,medical_dosage, medical_dosage_timing ):
        # Create the Prescription instance
        prescription = cls.objects.create(**prescription_data)


        # ---medical dosages---

        # Iterate over each item data to create PrescriptionItems and their dosages
        for item in items_data:
            item_instance = PrescriptionItem(
                prescription=prescription,
                item=item['item'],
                name=item['name']  # Assuming there's a 'name' field in PrescriptionItem
            )
            item_instance.save()

            # Handle dosages if provided
            for dosage_data in item.get('dosages', []):
                dosage_instance = MedicineDosage.objects.create(**dosage_data)
                item_instance.dosages.add(dosage_instance)

        return prescription


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


    