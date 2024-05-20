import uuid
from django.db import IntegrityError, models
from django.forms import ValidationError

from features.base.time_stamped_abstract_class import TimeStampedAbstractModelClass
from features.id_manager.models import IdManager
from features.item.models import Item
from features.medicine.models import MedicineDosage
from features.patient.models import Patient
from django.db import transaction

from features.user.models import CustomUser

PRESCRIPTION_ABBREVIATION = 'PRESC'
class Prescription(TimeStampedAbstractModelClass):
    
    class PresciptionDispenseStatus(models.TextChoices):
        DISPENSED = 'dispensed', 'Dispensed'
        NOT_DISPENSED = 'not_dispensed', 'Not Dispensed'
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code=models.CharField(max_length=255,unique=True)
    patient = models.ForeignKey(Patient, related_name='prescriptions_patient', on_delete=models.CASCADE)
    # doctor = models.ForeignKey(CustomUser, related_name='prescriptions_doctor', on_delete=models.CASCADE)
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
        if not self.code:
            self.code = self.generate_unique_code()
        # Use a transaction to ensure the save operation is atomic
        try:
            with transaction.atomic():
                super().save(*args, **kwargs)
        except IntegrityError:
            self.code = self.generate_unique_code()
            super().save(*args, **kwargs)
            
    def generate_unique_code(self):
        max_attempts = 10
        for _ in range(max_attempts):
            code = IdManager.generateId(prefix=PRESCRIPTION_ABBREVIATION)
            print(code)
            if not Prescription.objects.filter(code=code).exists():
                return code
        raise ValidationError("Unable to generate a unique code for the Prescription")


class PrescriptionItem(TimeStampedAbstractModelClass):
    dosages = models.ManyToManyField(MedicineDosage, related_name='dosages')
    medicine = models.ForeignKey(
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
    note=models.TextField(null=True, blank=True)

    class Meta:
        app_label = "prescription"


    