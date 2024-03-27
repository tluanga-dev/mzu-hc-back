
from django.db import models
from features.inventory_transaction.inventory_transaction.models import InventoryTransaction
from features.supplier.models import Supplier


class IndentInventoryTransaction(InventoryTransaction):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    supply_order_no = models.CharField(max_length=250, unique=True)
    supply_order_date = models.DateField()
    date_of_delivery = models.DateField()

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.inventory_transaction_type = self.TransactionTypes.INDENT
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'indent_transaction'
