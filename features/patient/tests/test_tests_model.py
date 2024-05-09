import uuid
from django.test import TestCase
from features.person.models import Person
from features.patient.models import Patient

class PatientModelTestCase(TestCase):
    def setUp(self):
        self.person = Person.objects.create(name='John Doe')
        self.patient = Patient.objects.create(
            mzu_user=self.person,
            patient_type='Employee',
            name='Test Patient',
            gender='Male',
            age=30,
            mzu_id='123456',
            mobile_number='1234567890',
            illness=['Fever', 'Cough'],
            allergy=['Pollen', 'Dust']
        )

    def test_patient_creation(self):
        self.assertIsInstance(self.patient, Patient)
        self.assertIsNotNone(self.patient.mzu_hc_id)
        self.assertEqual(self.patient.mzu_user, self.person)
        self.assertEqual(self.patient.patient_type, 'Employee')
        self.assertEqual(self.patient.name, 'Test Patient')
        self.assertEqual(self.patient.gender, 'Male')
        self.assertEqual(self.patient.age, 30)
        self.assertEqual(self.patient.mzu_id, '123456')
        self.assertEqual(self.patient.mobile_number, '1234567890')
        self.assertEqual(self.patient.illness, ['Fever', 'Cough'])
        self.assertEqual(self.patient.allergy, ['Pollen', 'Dust'])

    def test_patient_mzu_hc_id_generation(self):
        patient = Patient.objects.create(
            mzu_user=self.person,
            patient_type='Student',
            name='Another Patient',
            gender='Female',
            age=25,
            mzu_id='654321',
            mobile_number='9876543210',
            illness=['Headache'],
            allergy=['Pollen']
        )
        self.assertIsNotNone(patient.mzu_hc_id)
        self.assertNotEqual(patient.mzu_hc_id, self.patient.mzu_hc_id)

    def test_patient_save_method(self):
        patient = Patient(
            mzu_user=self.person,
            patient_type='Other',
            name='New Patient',
            gender='Male',
            age=40,
            mzu_id='789012',
            mobile_number='0987654321',
            illness=['Back Pain'],
            allergy=['Dust']
        )
        patient.save()
        self.assertIsNotNone(patient.mzu_hc_id)
        self.assertNotEqual(patient.mzu_hc_id, self.patient.mzu_hc_id)

        saved_patient = Patient.objects.get(pk=patient.pk)
        self.assertEqual(saved_patient.mzu_hc_id, patient.mzu_hc_id)

        patient.name = 'Updated Patient'
        patient.save()
        updated_patient = Patient.objects.get(pk=patient.pk)
        self.assertEqual(updated_patient.name, 'Updated Patient')import uuid
from django.test import TestCase
from features.person.models import Person
from features.patient.models import Patient

class PatientModelTestCase(TestCase):
    def setUp(self):
        self.person = Person.objects.create(name='John Doe')
        self.patient = Patient.objects.create(
            mzu_user=self.person,
            patient_type='Employee',
            name='Test Patient',
            gender='Male',
            age=30,
            mzu_id='123456',
            mobile_number='1234567890',
            illness=['Fever', 'Cough'],
            allergy=['Pollen', 'Dust']
        )

    # Existing test cases...

    def test_patient_save_method(self):
        patient = Patient(
            mzu_user=self.person,
            patient_type='Other',
            name='New Patient',
            gender='Male',
            age=40,
            mzu_id='789012',
            mobile_number='0987654321',
            illness=['Back Pain'],
            allergy=['Dust']
        )
        patient.save()
        self.assertIsNotNone(patient.mzu_hc_id)
        self.assertNotEqual(patient.mzu_hc_id, self.patient.mzu_hc_id)

        saved_patient = Patient.objects.get(pk=patient.pk)
        self.assertEqual(saved_patient.mzu_hc_id, patient.mzu_hc_id)

        patient.name = 'Updated Patient'
        patient.save()
        updated_patient = Patient.objects.get(pk=patient.pk)
        self.assertEqual(updated_patient.name, 'Updated Patient')

    def test_patient_mzu_hc_id_generation(self):
        patient = Patient.objects.create(
            mzu_user=self.person,
            patient_type='Student',
            name='Another Patient',
            gender='Female',
            age=25,
            mzu_id='654321',
            mobile_number='9876543210',
            illness=['Headache'],
            allergy=['Pollen']
        )
        self.assertIsNotNone(patient.mzu_hc_id)
        self.assertNotEqual(patient.mzu_hc_id, self.patient.mzu_hc_id)

    def test_patient_creation(self):
        self.assertIsInstance(self.patient, Patient)
        self.assertIsNotNone(self.patient.mzu_hc_id)
        self.assertEqual(self.patient.mzu_user, self.person)
        self.assertEqual(self.patient.patient_type, 'Employee')
        self.assertEqual(self.patient.name, 'Test Patient')
        self.assertEqual(self.patient.gender, 'Male')
        self.assertEqual(self.patient.age, 30)
        self.assertEqual(self.patient.mzu_id, '123456')
        self.assertEqual(self.patient.mobile_number, '1234567890')
        self.assertEqual(self.patient.illness, ['Fever', 'Cough'])
        self.assertEqual(self.patient.allergy, ['Pollen', 'Dust'])

    def test_patient_model_fields(self):
        patient = Patient(
            mzu_user=self.person,
            patient_type='Employee Dependent',
            name='Another Test Patient',
            gender='Female',
            age=35,
            mzu_id='987654',
            mobile_number='0987654321',
            illness=['Headache', 'Fever'],
            allergy=['Dust', 'Pollen']
        )
        self.assertEqual(patient.mzu_user, self.person)
        self.assertEqual(patient.patient_type, 'Employee Dependent')
        self.assertEqual(patient.name, 'Another Test Patient')
        self.assertEqual(patient.gender, 'Female')
        self.assertEqual(patient.age, 35)
        self.assertEqual(patient.mzu_id, '987654')
        self.assertEqual(patient.mobile_number, '0987654321')
        self.assertEqual(patient.illness, ['Headache', 'Fever'])
        self.assertEqual(patient.allergy, ['Dust', 'Pollen'])