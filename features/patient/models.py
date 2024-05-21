import uuid
from django.db import models
from django.core.exceptions import ValidationError
from features.person.models import Employee, EmployeeDependent, MZUOutsider, Student

class Patient(models.Model):
    """Model representing a patient in the system."""
    # UUID field as a health centre ID
    mzu_hc_id = models.UUIDField(default=uuid.uuid4, editable=False)

    # Link to a Person model
    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING, null=True, blank=True)
    employee_dependent = models.ForeignKey(EmployeeDependent, on_delete=models.DO_NOTHING, null=True, blank=True)
    mzu_outsider = models.ForeignKey(MZUOutsider, on_delete=models.DO_NOTHING, null=True, blank=True)

    # Choices for type of patient
    PATIENT_TYPE_CHOICES = [
        ('Employee', 'Employee'),
        ('Employee Dependent', 'Employee Dependent'),
        ('Student', 'Student'),
        ('MZU_outsider', 'MZU_outsider'),
    ]
    patient_type = models.CharField(max_length=255, choices=PATIENT_TYPE_CHOICES)

    illness = models.JSONField(blank=True, null=True, default=list)
    allergy = models.JSONField(blank=True, null=True, default=list)

    def clean(self):
        """Validates the patient instance before saving."""
        # Validate patient type and related fields
        if self.patient_type == 'Employee Dependent' and not self.employee_dependent:
            raise ValidationError("Employee Dependent patients must have an associated employee dependent.")
        if self.patient_type == 'Student' and not self.student:
            raise ValidationError("Student patients must have an associated student.")
        if self.patient_type == 'Other' and not self.mzu_outsider:
            raise ValidationError("Other patients must have an associated MZU outsider patient.")
        if self.patient_type == 'Employee' and not self.employee:
            raise ValidationError("Employee patients must have an associated employee.")

        # Ensure only one type of related person is set
        related_fields = [self.employee, self.employee_dependent, self.student, self.mzu_outsider]
        if sum(bool(field) for field in related_fields) > 1:
            raise ValidationError("A patient can only be associated with one related person (employee, employee dependent, student, or MZU outsider).")

        # Validate patient type choice
        if self.patient_type not in dict(self.PATIENT_TYPE_CHOICES):
            raise ValidationError("Invalid patient_type value.")

    def save(self, *args, **kwargs):
        """Overrides the save method to include validation."""
        self.full_clean()  # This will call the clean method
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Patient {self.mzu_hc_id} ({self.patient_type})"

    class Meta:
        app_label = "patient"
        verbose_name = "Patient"
        verbose_name_plural = "Patients"
