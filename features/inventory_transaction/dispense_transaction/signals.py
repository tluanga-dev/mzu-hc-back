from django.dispatch import receiver
from django.db.models.signals import post_save

from features.inventory_transaction.dispense_transaction.models import DispenseInventoryTransaction
from features.prescription.models import Prescription


@receiver(post_save, sender=DispenseInventoryTransaction)
def post_save_inventory_transaction_item(sender, instance, created, **kwargs):
    print('DispenseInventoryTransaction created' )
    if created:
        # update the prescription status to dispensed
        try:
            prescription=instance.prescription
            prescription.prescription_dispense_status=Prescription.PresciptionDispenseStatus.DISPENSED
            prescription.save()
        except Exception as e:
            print(f"Error: {e}")
            