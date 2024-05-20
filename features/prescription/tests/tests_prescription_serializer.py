from django.test import TestCase
from rest_framework.exceptions import ValidationError
from features.patient.serializers import CreatePatientPrescriptionSerializer
from features.person.models import Employee, Student, EmployeeDependent, MZUOutsider, OrganisationUnit

class CreatePatientPrescriptionSerializerTest(TestCase):
    def setUp(self):
        self.organisation_unit = OrganisationUnit.objects.create(
            name="Test Unit", description="Test Description", abbreviation="TU"
        )
        self.employee = Employee.objects.create(
            name="John Doe", gender="Male", date_of_birth="1980-01-01",
            organisation_unit=self.organisation_unit, mobile_no=1234567890,
            email="john@example.com", employee_type="Teaching",
            mzu_employee_id="EMP123", designation="Professor"
        )
        self.student = Student.objects.create(
            name="Jane Smith", gender="Female", date_of_birth="1995-01-01",
            organisation_unit=self.organisation_unit, mobile_no=1234567891,
            email="jane@example.com", mzu_student_id="STU123",
            programme="MSc", year_of_admission=2020
        )

    def test_create_patient_prescription_for_employee(self):
        data = {
            "patient_type": "Employee",
            "patient_data": {
                "illness": ["Flu"],
                "allergy": ["Peanuts"],
                "gender": "Male",
                "employee": self.employee.id
            },
            "prescription_data": {
                "chief_complaints": "Headache",
                "diagnosis": "Migraine",
                "advice_and_instructions": "Rest and hydrate",
                "note": "Avoid stress",
                "date_and_time": "2024-05-18T12:00:00Z",
                "prescription_dispense_status": "not_dispensed"
            }
        }
        serializer = CreatePatientPrescriptionSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        result = serializer.save()
        self.assertIn('patient', result)
        self.assertIn('prescription', result)

    def test_create_patient_prescription_for_new_mzu_outsider(self):
        data = {
            "patient_type": "Other",
            "patient_data": {
                "illness": ["Hypertension"],
                "allergy": ["None"],
                "gender": "Male"
            },
            "prescription_data": {
                "chief_complaints": "High blood pressure",
                "diagnosis": "Hypertension",
                "advice_and_instructions": "Take medication daily",
                "note": "Regular check-ups",
                "date_and_time": "2024-05-18T12:00:00Z",
                "prescription_dispense_status": "not_dispensed"
            },
            "mzu_outsider_data": {
                "name": "John Doe",
                "gender": "Male",
                "age": 45
            }
        }
        serializer = CreatePatientPrescriptionSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        result = serializer.save()
        self.assertIn('patient', result)
        self.assertIn('prescription', result)

    def test_invalid_patient_type(self):
        data = {
            "patient_type": "InvalidType",
            "patient_data": {
                "illness": ["Hypertension"],
                "allergy": ["None"],
                "gender": "Male"
            },
            "prescription_data": {
                "chief_complaints": "High blood pressure",
                "diagnosis": "Hypertension",
                "advice_and_instructions": "Take medication daily",
                "note": "Regular check-ups",
                "date_and_time": "2024-05-18T12:00:00Z",
                "prescription_dispense_status": "not_dispensed"
            }
        }
        serializer = CreatePatientPrescriptionSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('patient_type', serializer.errors)
