import uuid
from django.db import models

from features.base.time_stamped_abstract_class import TimeStampedAbstractModelClass
from features.id_manager.models import IdManager
from features.item.models import Item
from features.person.models import Person

PRESCRIPTION_ABBREVIATION = 'PRESC'
class Prescription(TimeStampedAbstractModelClass):
    
    class PresciptionDispenseStatus(models.TextChoices):
        DISPENSED = 'dispensed', 'Dispensed'
        NOT_DISPENSED = 'not_dispensed', 'Not Dispensed'
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code=models.CharField(max_length=255,unique=True)
    patient = models.ForeignKey(Person, related_name='prescriptions_patient', on_delete=models.CASCADE)
    doctor = models.ForeignKey(Person, related_name='prescriptions_doctor', on_delete=models.CASCADE)
    chief_complaint=models.TextField()
    diagnosis=models.TextField()
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
        if not self.code:
            
            generated_item_code = IdManager.generateId(PRESCRIPTION_ABBREVIATION)
            # print(generated_item_code)
            self.code = generated_item_code

        super().save(*args, **kwargs)
    class Meta:
        app_label = "prescription"


class PrescribedMedicine(TimeStampedAbstractModelClass):
    medicine = models.ForeignKey(
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
        on_delete=models.DO_NOTHING
    )

    duration_value=models.IntegerField(blank=True, null=True)
    duration_type = models.CharField(max_length=10, choices=DURATION_CHOICES, default='days')
    prescribedMedicine=models.ForeignKey(PrescribedMedicine,on_delete=models.CASCADE)



    class Meta:
        app_label = "prescription"

class MedicineDosageElement(TimeStampedAbstractModelClass):
    amount = models.IntegerField()
    # dayMedSchedule can have values like-morning, afternoon, evening,noon
    dayMedSchedule = models.CharField(max_length=255)
    # medicineTiming can have values like- before meal, after meal, na
    medicineTiming = models.CharField(max_length=255)
    medicine_dosage=models.ForeignKey(MedicineDosage,on_delete=models.CASCADE)
   
    class Meta:
        app_label = "prescription"







    