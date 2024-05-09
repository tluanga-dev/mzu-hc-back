from django.test import TestCase
from features.patient.models import Patient

class PatientModelTest(TestCase):
    def setUp(self):
        self.patient_data = {
            'patient_type': 'Employee',
            'name': 'John Doe',
            'gender': 'Male',
            'age': 30,
            'mzu_id': 'MZU123',
            'mobile_number': '1234567890',
            'illness': ['Fever', 'Cough'],
            'allergy': ['Pollen', 'Dust'],
        }
        self.patient = Patient.objects.create(**self.patient_data)

    def test_patient_creation(self):
        self.assertEqual(self.patient.patient_type, self.patient_data['patient_type'])
        self.assertEqual(self.patient.name, self.patient_data['name'])
        self.assertEqual(self.patient.gender, self.patient_data['gender'])
        self.assertEqual(self.patient.age, self.patient_data['age'])
        self.assertEqual(self.patient.mzu_id, self.patient_data['mzu_id'])
        self.assertEqual(self.patient.mobile_number, self.patient_data['mobile_number'])
        self.assertEqual(self.patient.illness, self.patient_data['illness'])
        self.assertEqual(self.patient.allergy, self.patient_data['allergy'])