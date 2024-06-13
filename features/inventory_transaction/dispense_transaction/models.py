
from django.db import models
from features.base.time_stamped_abstract_class import TimeStampedAbstractModelClass
from features.inventory_transaction.inventory_transaction.models import InventoryTransaction
from features.item.models import Item
from features.patient.models import Patient
from features.prescription.models import Prescription


# -Dispense medicine to patient
class DispenseInventoryTransaction(InventoryTransaction):
    # dispense_date=models.DateField()
    # prescription=models.ForeignKey(
    #     Prescription, on_delete=models.CASCADE, related_name='dispened_prescription')
    patient = models.ForeignKey(
        Patient, 
        related_name='dispense_patient', 
        on_delete=models.DO_NOTHING)
    pharmacist=models.CharField(max_length=255)
    prescription=models.ForeignKey(
        Prescription, 
        related_name='dispensed_prescription', 
        on_delete=models.DO_NOTHING)
    
    def save(self, *args, **kwargs):
        if self.pk is None:
            self.inventory_transaction_type = self.TransactionTypes.DISPENSE
        super().save(*args, **kwargs)
   
    class Meta:
        app_label = 'dispense_transaction'

