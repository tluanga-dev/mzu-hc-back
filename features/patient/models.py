import uuid
from django.db import models
from features.person.models import Employee, EmployeeDependent, Person, Student
from datetime import datetime

class Patient(models.Model):
    # UUID field as a health centre ID
    mzu_hc_id = models.UUIDField(default=uuid.uuid4, editable=False)
    # Link to a Person model
    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING, null=True, blank=True)
    employee_dependent = models.ForeignKey(EmployeeDependent, on_delete=models.DO_NOTHING, null=True, blank=True)
    # Choices for type of patient
    PATIENT_TYPE_CHOICES = [
        ('Employee', 'Employee'),
        ('Employee Dependent', 'Employee Dependent'),
        ('Student', 'Student'),
        ('Other', 'Other'),
    ]
    patient_type = models.CharField(max_length=255, choices=PATIENT_TYPE_CHOICES)
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    # Automatically computed year of birth
    year_of_birth = models.IntegerField(editable=False)
    mzu_student_id = models.CharField(max_length=255, blank=True, null=True)
    mobile_number = models.CharField(max_length=255, blank=True, null=True)
    illness = models.JSONField(blank=True, null=True, default=list)
    allergy = models.JSONField(blank=True, null=True, default=list)

    @property
    def age(self):
        return datetime.now().year - self.year_of_birth

    @age.setter
    def age(self, value):
        current_year = datetime.now().year
        self.year_of_birth = current_year - value

    def save(self, *args, **kwargs):
        # Check if patient already exists
        existing_patients = Patient.objects.filter(name=self.name, gender=self.gender, year_of_birth=self.year_of_birth)
        if existing_patients.exists():
            raise ValueError("Patient already exists in the system.")
            return existing_patients.first()

        # Other validations based on patient type
        if self.patient_type == 'Employee Dependent':
            if not self.mzu_user:
                raise ValueError("mzu_user is required for Employee Dependent patients.")
            if self.student_id or self.mobile_number:
                raise ValueError("student_id and mobile_number are not required for Employee Dependent patients.")
        elif self.patient_type == 'Student':
            if not self.student_id:
                raise ValueError("student_id is required for Student patients.")
        elif self.patient_type == 'Other':
            if not self.mobile_number:
                raise ValueError("mobile_number is required for Other patients.")
            if self.student_id or self.mzu_user:
                raise ValueError("student_id and mzu_user are not required for Other patients.")
        elif self.patient_type == 'Employee':
            if not self.mzu_user:
                raise ValueError("mzu_user is required for Employee patients.")
            if self.student_id or self.mobile_number:
                raise ValueError("student_id and mobile_number are not required for Employee patients.")
            
        if not self.patient_type in dict(self.PATIENT_TYPE_CHOICES).keys():
            raise ValueError("Invalid patient_type value.")

        super().save(*args, **kwargs)

    class Meta:
        app_label = "patient"
