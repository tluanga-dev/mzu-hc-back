import uuid
from django.db import models

from features.base.time_stamped_abstract_class import TimeStampedAbstractModelClass

class Supplier(TimeStampedAbstractModelClass):
    name = models.CharField(max_length=255)
    contact_no = models.FloatField()
    email = models.EmailField(max_length=255)
    address = models.TextField()
    remarks = models.TextField(blank=True, null=True)


    class Meta:
        app_label = 'supplier'