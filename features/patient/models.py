import uuid
from features.base.time_stamped_abstract_class import TimeStampedAbstractModelClass
from django.db import models
from features.person.models import Person


class Patient(TimeStampedAbstractModelClass):
    # --Health Centre Id
    mzu_hc_id = models.UUIDField(default=uuid.uuid4, editable=False)
    mzu_user = models.ForeignKey(Person, on_delete=models.DO_NOTHING, null=True, blank=True)
    PATIENT_TYPE_CHOICES = [
        ('Employee', 'Employee'),
        ('Employee Dependent', 'Employee Dependent'),
        ('Student', 'Student'),
        ('Other', 'Other'),
    ]
    patient_type = models.CharField(max_length=255, choices=PATIENT_TYPE_CHOICES)
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    age = models.IntegerField(blank=True, null=True)
    student_id = models.CharField(max_length=255, blank=True, null=True)
    mobile_number = models.CharField(max_length=255, blank=True, null=True)
    illness = models.JSONField(blank=True, null=True, default=list)
    allergy = models.JSONField(blank=True, null=True, default=list)
    
    def save(self, *args, **kwargs):
        if self.patient_type == 'Other':
            self.mzu_user = None
        if not self.mzu_hc_id:
            self.mzu_hc_id = uuid.uuid4().hex[:8]

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
