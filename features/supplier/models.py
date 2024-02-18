import uuid
from django.db import models

from features.base.time_stamped_abstract_class import TimeStampedAbstractModelClass

class Supplier(TimeStampedAbstractModelClass):
    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=255)
    contact_no = models.PositiveBigIntegerField(null=True, blank=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)


    class Meta:
        app_label = 'supplier'