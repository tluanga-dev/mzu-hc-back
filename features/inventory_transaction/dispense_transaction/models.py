
from django.db import models
from features.inventory_transaction.inventory_transaction.models import InventoryTransaction
from features.person.models import Person
from features.prescription.models import Prescription
from features.supplier.models import Supplier

# -Dispense medicine to patient
class DispenseInventoryTransaction(InventoryTransaction):
    dispense_date=models.DateField()
    prescription=models.ForeignKey(
        Prescription, on_delete=models.CASCADE, related_name='dispened_prescription')

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.inventory_transaction_type = self.TransactionTypes.DISPENSE
        super().save(*args, **kwargs)
   
    class Meta:
        app_label = 'dispense_transaction'
