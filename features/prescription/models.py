import uuid
from django.db import IntegrityError, models, transaction
from django.core.exceptions import ValidationError
from django.utils.timezone import make_aware
from django.db.models.signals import post_init
from django.dispatch import receiver

from features.base.time_stamped_abstract_class import TimeStampedAbstractModelClass
from features.id_manager.models import IdManager
from features.item.models import Item
from features.medicine.models import MedicineDosage
from features.patient.models import Patient
from features.user.models import CustomUser

PRESCRIPTION_ABBREVIATION = 'PRESC'


class Prescription(TimeStampedAbstractModelClass):
    
    class PrescriptionDispenseStatus(models.TextChoices):
        DISPENSED = 'dispensed', 'Dispensed'
        NOT_DISPENSED = 'not_dispensed', 'Not Dispensed'
    
    code = models.CharField(max_length=255, unique=True, blank=True)
    patient = models.ForeignKey(Patient, related_name='prescriptions_patient', on_delete=models.CASCADE)
    chief_complaints = models.TextField()
    diagnosis = models.TextField()
    advice_and_instructions = models.TextField()
    note = models.TextField(blank=True, default='')
    date_and_time = models.DateTimeField()
    prescription_dispense_status = models.CharField(
        max_length=100, 
        choices=PrescriptionDispenseStatus.choices, 
        default=PrescriptionDispenseStatus.NOT_DISPENSED
    )

    # def get_prescribed_medicine_by_patient(self, patient_id):
    #     return self.prescribed_medicine_set.filter(prescription__patient_id=patient_id)
    
    def save(self, *args, **kwargs):
        self.date_and_time = self.make_datetime_aware(self.date_and_time)
        
        if not self.code:
            self.code = self.generate_unique_code()

        for attempt in range(10):
            try:
                with transaction.atomic():
                    # Check if the code is unique within the transaction
                    if Prescription.objects.filter(code=self.code).exists():
                        self.code = self.generate_unique_code()
                    super().save(*args, **kwargs)
                return
            except IntegrityError as e:
                if attempt == 9:
                    # Log the error here if logging is configured
                    raise ValidationError(f"Unable to save Prescription: {e}")


    def generate_unique_code(self):
        for _ in range(10):
            code = IdManager.generateId(prefix=PRESCRIPTION_ABBREVIATION)
            if not Prescription.objects.filter(code=code).exists():
                return code
        raise ValidationError("Unable to generate a unique code for the Prescription after multiple attempts")

    @staticmethod
    def make_datetime_aware(dt):
        if dt and dt.tzinfo is None:
            return make_aware(dt)
        return dt

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
        related_name='prescribed_item_set',
        on_delete=models.CASCADE
    )
    note = models.TextField(null=True, blank=True)

    class Meta:
        app_label = "prescription"

