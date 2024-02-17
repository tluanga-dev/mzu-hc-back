

from django.test import TestCase
from features.base.base_test_setup_class import BaseTestCase
from features.item.models import Item

from features.person.models import Department, Person, PersonType
from features.prescription.models import PrescribedMedicine, Prescription



class TestModels(BaseTestCase):
    def setUp(self):
        super().setUp()
        Person.objects.all().delete()
        self.item = Item.objects.create(
            name="Test Item",
            description="Test Description",
            type=self.item_type,
            unit_of_measurement=self.unit_of_measurement,
            is_active=True
        )
        self.person_type_patient = PersonType.objects.create(
            name='Patient',
            description='Patient',
            is_active=True
        )
        self.person_type_doctor = PersonType.objects.create(
            name='Doctor',
            description='Doctor',
            is_active=True
        )
        self.department = Department.objects.create(
            name='Test Department',
            description='Test Description',
            is_active=True
        )
        self.patient = Person.objects.create(
            name='Test Patient',
            person_type=self.person_type_patient,
            department=self.department,
            email='test@gmail.com',
            mzu_id='123456',
            is_active=True,
            contact_no=1234567890
        )
        self.doctor = Person.objects.create(
            name='Test Doctor',
            person_type=self.person_type_doctor,
            department=self.department,
            email='doctor@gmail.com',
            mzu_id='1234561212',
            is_active=True,
            contact_no=1234567890
        )
        
    
    def test_prescription_creation(self):
        self.prescription=Prescription.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            date_and_time='2021-01-01',
            prescription_dispense_status=Prescription.PressciptionDispenseStatus.NOT_DISPENSED,
            note='Test Note',
        )

        # ---create prescription Item
        self.prescription_item1=PrescribedMedicine.objects.create(
            prescription=self.prescription,
            item=self.item,
            dosage='test dosage',
            is_active=True
        )
        
        self.assertEqual(Prescription.objects.all().count(), 1)
        self.assertEqual(Prescription.objects.get(id=self.prescription.id).patient, self.patient)