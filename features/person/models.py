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
    abbreviation=models.TextField()
    class Meta:
        app_label = "person"

class Person(TimeStampedAbstractModelClass):
    name= models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=False, null=False, blank=False)
    mzu_id = models.CharField(max_length=255, unique=True)
    date_of_birth = models.DateField(blank=True, null=True)
    department=models.CharField(max_length=255, blank=True, null=True)
    designation=models.CharField(max_length=255, blank=True, null=True)
    person_type=models.ForeignKey(PersonType, on_delete=models.CASCADE)
    mobile_no=models.PositiveBigIntegerField(null=True, blank=True)
 
    class Meta:
        app_label = "person"

class Patient(Person):
    illness = models.JSONField(blank=True, null=True, default=list)
    allergy = models.JSONField(blank=True, null=True, default=list)

    class Meta:
        app_label = "person"
        proxy = True