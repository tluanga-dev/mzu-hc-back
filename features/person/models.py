from django.db import models

from features.base.time_stamped_abstract_class import TimeStampedAbstractModelClass

class Department(TimeStampedAbstractModelClass):
    name = models.CharField(max_length=255)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        app_label = "person"

class PersonType(TimeStampedAbstractModelClass):
    name = models.CharField(max_length=255)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        app_label = "person"


class Person(TimeStampedAbstractModelClass):
    name= models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    mzu_id = models.CharField(max_length=255, unique=True)
    department=models.ForeignKey(Department, on_delete=models.CASCADE)
    person_type=models.ForeignKey(PersonType, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    class Meta:
        app_label = "person"
