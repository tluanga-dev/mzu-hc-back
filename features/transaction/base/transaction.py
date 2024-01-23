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
    status = models.CharField(max_length=10, default='pending')