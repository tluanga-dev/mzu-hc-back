import uuid
from django.db import models

from features.base.time_stamped_abstract_class import TimeStampedAbstractModelClass
from features.common.utils.calculate_age_3 import get_age_3
from features.common.utils.convert_date import DateConverter
from features.organisation_unit.models import OrganisationUnit

from datetime import date



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
    organisation_unit=models.ForeignKey(
        OrganisationUnit, 
        on_delete=models.DO_NOTHING, 
        related_name='%(class)s_organization_unit',
        null=True, 
        blank=True
    )
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
    def get_name(cls):
        return cls.name
    
    # def get_age(self):
    #     if self.date_of_birth:
    #         # calculate_age
    #         def calculate_age(date_of_birth):
    #             today = date.today()
    #             age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
    #             return age

    #         age = calculate_age(self.date_of_birth)
    #         return age
            
    #     return None
    
    def get_age(self):
        if self.date_of_birth:
            # calculate_age
            age = get_age_3(self.date_of_birth)
            return age
        return None

    def save(self, *args, **kwargs):
        if isinstance(self.date_of_birth, str):
            self.date_of_birth = DateConverter.convert_to_date_field(self.date_of_birth)
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
# ------------Employee Part----------------
class Employee(Person):
    EMPLOYEE_TYPE_CHOICES = [
        ('Teaching', 'Teaching'),
        ('Non-Teaching', 'Non-Teaching'),
    
    ]
    employee_type=models.CharField(max_length=255,choices=EMPLOYEE_TYPE_CHOICES)
    mzu_employee_id = models.CharField(max_length=255, unique=True)
    designation = models.CharField(max_length=255)

    def get_age(self):
        if self.date_of_birth:
            # calculate_age
            age = get_age_3(self.date_of_birth)
            return age
    def get_mzu_employee_id(self):
        return self.mzu_employee_id
    class Meta:
        app_label = "person"

class EmployeeDependent(TimeStampedAbstractModelClass):
    mzu_employee_dependent_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    name = models.CharField(max_length=255)
    gender=models.CharField(max_length=255)
    date_of_birth = models.DateField(blank=True, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employee_dependents')
    relation = models.CharField(max_length=255)
    def save(self, *args, **kwargs):
        if isinstance(self.date_of_birth, str):
            self.date_of_birth = DateConverter.convert_to_date_field(self.date_of_birth)
        super().save(*args, **kwargs)
    def get_name(cls):
        return cls.name
    def get_age(self):
        if self.date_of_birth:
            # calculate_age
            age = get_age_3(self.date_of_birth)
            return age
        return None

# --Student Part--
class Student(Person):
    mzu_student_id = models.CharField(max_length=255, unique=True)
    programme=models.CharField(max_length=255,null=True, blank=True)
    year_of_admission=models.PositiveIntegerField(null=True, blank=True)
    


    class Meta:
        app_label = "person"

class MZUOutsider(TimeStampedAbstractModelClass):
    GENDER_TYPE_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    name= models.CharField(max_length=255)
    gender = models.CharField(max_length=255, choices=GENDER_TYPE_CHOICES)
    age = models.PositiveIntegerField()
    date_of_birth = models.DateField(blank=True, null=True)

    def get_age(self):
        if self.date_of_birth:
            # calculate_age
            age = get_age_3(self.date_of_birth)
            return age
        return None

    def save(self, *args, **kwargs):
        if isinstance(self.date_of_birth, str):
            self.date_of_birth = DateConverter.convert_to_date_field(self.date_of_birth)
        super().save(*args, **kwargs)
    def get_name(cls):
        print('getting name for outsider')
        name=cls.name
        print(name)
        return name
    class Meta:
        app_label = "person"
