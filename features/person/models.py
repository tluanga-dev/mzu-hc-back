import uuid
from django.db import models

from features.base.time_stamped_abstract_class import TimeStampedAbstractModelClass
from features.utils.convert_date import DateConverter

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
    gender = models.CharField(max_length=255, blank=True, null=True)
    mzu_id = models.CharField(max_length=255, unique=True)
    date_of_birth = models.DateField(blank=True, null=True)
    department=models.CharField(max_length=255, blank=True, null=True)
    designation=models.CharField(max_length=255, blank=True, null=True)
    person_type=models.ForeignKey(PersonType, on_delete=models.CASCADE)
    mobile_no=models.PositiveBigIntegerField(null=True, blank=True)
    email = models.EmailField(max_length=255, unique=False, null=False, blank=False)

    def formatted_date_of_birth(self):
        # Returns the date in dd-mm-yyyy format if the date is not None
        return self.date_of_birth.strftime('%d-%m-%Y') if self.date_of_birth else None
 
    @classmethod
    def create(cls, **kwargs):
        if 'date_of_birth' in kwargs and isinstance(kwargs['date_of_birth'], str):
            kwargs['date_of_birth'] = DateConverter.convert_to_date_field(kwargs['date_of_birth'])
        instance = cls(**kwargs)
        instance.full_clean()  # Validates model fields before saving
        instance.save()
        return instance

    def save(self, *args, **kwargs):
        if isinstance(self.date_of_birth, str):
            self.date_of_birth = DateConverter.convert_to_date_field(self.date_of_birth)
        super().save(*args, **kwargs)

    class Meta:
        app_label = "person"

