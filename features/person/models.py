import uuid
from django.db import models

from features.base.time_stamped_abstract_class import TimeStampedAbstractModelClass

class Department(TimeStampedAbstractModelClass):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        app_label = "person"

class PersonType(TimeStampedAbstractModelClass):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        app_label = "person"

class Person(TimeStampedAbstractModelClass):
    name= models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
    mzu_id = models.CharField(max_length=255, unique=True)
    department=models.ForeignKey(Department, on_delete=models.CASCADE)
    person_type=models.ForeignKey(PersonType, on_delete=models.CASCADE)
    contact_no=models.PositiveBigIntegerField(null=True, blank=True)
 
    class Meta:
        app_label = "person"
