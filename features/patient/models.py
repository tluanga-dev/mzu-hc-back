import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from features.base.time_stamped_abstract_class import TimeStampedAbstractModelClass
from features.person.models import Employee, EmployeeDependent, MZUOutsider, Student
from django.db import transaction
from django.db.models import Q

class Patient(TimeStampedAbstractModelClass):
    """Model representing a patient in the system."""
    
    class PatientType(models.TextChoices):
        EMPLOYEE = 'Employee', _('Employee')
        EMPLOYEE_DEPENDENT = 'Employee Dependent', _('Employee Dependent')
        STUDENT = 'Student', _('Student')
        MZU_OUTSIDER = 'MZU_outsider', _('MZU Outsider')

    mzu_hc_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    employee = models.OneToOneField(Employee, on_delete=models.DO_NOTHING, null=True, blank=True, unique=True)
    student = models.OneToOneField(Student, on_delete=models.DO_NOTHING, null=True, blank=True, unique=True)
    employee_dependent = models.OneToOneField(EmployeeDependent, on_delete=models.DO_NOTHING, null=True, blank=True, unique=True)
    mzu_outsider = models.OneToOneField(MZUOutsider, on_delete=models.DO_NOTHING, null=True, blank=True, unique=True)

    patient_type = models.CharField(max_length=255, choices=PatientType.choices)

    illness = models.JSONField(blank=True, null=True, default=list)
    allergy = models.JSONField(blank=True, null=True, default=list)

    class Meta:
        app_label = "patient"
        verbose_name = "Patient"
        verbose_name_plural = "Patients"
        indexes = [
            models.Index(fields=['mzu_hc_id']),
            models.Index(fields=['patient_type']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['employee', 'student', 'employee_dependent', 'mzu_outsider'],
                name='unique_patient'
            )
        ]
        ordering = ['-created_at']

    def clean(self):
        """Validates the patient instance before saving."""
        # Validate patient type and related fields
        if self.patient_type == self.PatientType.EMPLOYEE_DEPENDENT and not self.employee_dependent:
            raise ValidationError(_("Employee Dependent patients must have an associated employee dependent."))
        if self.patient_type == self.PatientType.STUDENT and not self.student:
            raise ValidationError(_("Student patients must have an associated student."))
        if self.patient_type == self.PatientType.MZU_OUTSIDER and not self.mzu_outsider:
            raise ValidationError(_("MZU Outsider patients must have an associated MZU outsider."))
        if self.patient_type == self.PatientType.EMPLOYEE and not self.employee:
            raise ValidationError(_("Employee patients must have an associated employee."))

        # Ensure only one type of related person is set
        related_fields = [self.employee, self.employee_dependent, self.student, self.mzu_outsider]
        if sum(bool(field) for field in related_fields) > 1:
            raise ValidationError(_("A patient can only be associated with one related person (employee, employee dependent, student, or MZU outsider)."))

        # Validate patient type choice
        if self.patient_type not in self.PatientType.values:
            raise ValidationError(_("Invalid patient_type value."))

    def save(self, *args, **kwargs):
        """Overrides the save method to include validation."""
        self.full_clean()  # This will call the clean method
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Patient {self.mzu_hc_id} ({self.get_patient_type_display()})"
    
    @property
    def related_person(self):
        """Returns the related person object based on the patient type."""
        if self.patient_type == self.PatientType.EMPLOYEE:
            return self.employee
        if self.patient_type == self.PatientType.EMPLOYEE_DEPENDENT:
            return self.employee_dependent
        if self.patient_type == self.PatientType.STUDENT:
            return self.student
        if self.patient_type == self.PatientType.MZU_OUTSIDER:
            return self.mzu_outsider
        return None
