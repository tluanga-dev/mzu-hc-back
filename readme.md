from django.db import models

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('indent', 'Indent'),
        ('dispense', 'Dispense'),
        ('dispose', 'Dispose'),
    ]
    
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    transaction_id = models.CharField(max_length=20, unique=True)
    date_time = models.DateTimeField(auto_now_add=True)
    initiated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, default='pending')
    
    # Indent Transaction specific fields
    requested_quantity = models.IntegerField(blank=True, null=True)
    supplier_details = models.CharField(max_length=100, blank=True)
    
    # Dispense Transaction specific fields
    dispensed_quantity = models.IntegerField(blank=True, null=True)
    recipient_details = models.CharField(max_length=100, blank=True)
    
    # Dispose Transaction specific fields
    disposed_quantity = models.IntegerField(blank=True, null=True)
    disposal_method = models.CharField(max_length=100, blank=True)
