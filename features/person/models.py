import uuid
from django.db import models

from features.base.time_stamped_abstract_class import TimeStampedAbstractModelClass
from features.utils.convert_date import DateConverter



class User(TimeStampedAbstractModelClass):
    USER_TYPE_CHOICES = [
        ('Doctor', 'Doctor '),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    name= models.CharField(max_length=255)
    designation=models.CharField(max_length=255)
    user_type=models.CharField(max_length=255,choices=USER_TYPE_CHOICES)




class Person(TimeStampedAbstractModelClass):
    GENDER_TYPE_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    PERSON_TYPE_CHOICES = [
        ('Employee', 'Employee'),
        ('Employee Dependent', 'Employee Dependent'),
        ('Student', 'Student'),
    ]
    name= models.CharField(max_length=255)
    gender = models.CharField(max_length=255, choices=GENDER_TYPE_CHOICES)
    date_of_birth = models.DateField(blank=True, null=True)
    department=models.CharField(max_length=255, blank=True, null=True)
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
        abstract = True
# ------------Employee Part----------------
class Employee(Person):
    EMPLOYEE_TYPE_CHOICES = [
        ('Employee', 'Employee'),
        ('Employee Dependent', 'Employee Dependent'),
        ('Student', 'Student'),
    ]
    employee_type=models.CharField(max_length=255,choices=EMPLOYEE_TYPE_CHOICES)
    mzu_employee_id = models.CharField(max_length=255, unique=True)
    designation = models.CharField(max_length=255)

    class Meta:
        app_label = "person"

class EmployeeDependent(TimeStampedAbstractModelClass):
    name = models.CharField(max_length=255)
    relation = models.CharField(max_length=255)
    date_of_birth = models.DateField(blank=True, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employee_dependents')


# --Student Part--
class Student(Person):
    mzu_student_id = models.CharField(max_length=255, unique=True)
    department = models.CharField(max_length=255)
    class Meta:
        app_label = "person"


