from django.test import TestCase

from features.patient.models import Patient


class PatientModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Patient.objects.create(name='John Doe', age=30)

    def test_name_content(self):
        patient = Patient.objects.get(id=1)
        expected_object_name = f'{patient.name}'
        self.assertEquals(expected_object_name, 'John Doe')

    def test_age_content(self):
        patient = Patient.objects.get(id=1)
        expected_object_age = patient.age
        self.assertEquals(expected_object_age, 30)