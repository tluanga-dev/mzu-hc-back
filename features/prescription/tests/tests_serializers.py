from django.utils import timezone
import datetime
from features.base.base_test_setup_class import BaseTestCase
from features.item.models import Item
from features.person.models import Department, Person, PersonType
from features.prescription.models import PrescriptionItem, Prescription
from features.prescription.serializers import PrescriptionSerializer
from features.utils.print_json import print_json_string


class TestPrescription(BaseTestCase):
    def setUp(self):
        super().setUp()
        # Clear out previous test data for consistency
        Person.objects.all().delete()
        Prescription.objects.all().delete()
        PrescriptionItem.objects.all().delete()
        
        # Create test items
        self.item_1 = Item.objects.create(
            name="Test Item 1",
            description="Test Description 1",
            type=self.item_type,
            unit_of_measurement=self.unit_of_measurement,
            is_active=True
        )
        self.item_2 = Item.objects.create(
            name="Test Item 2",
            description="Test Description 2",
            type=self.item_type,
            unit_of_measurement=self.unit_of_measurement,
            is_active=True
        )
        
        # Create person types and department
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
        
        # Create patient and doctor
        self.patient = Person.objects.create(
            name='Test Patient',
            person_type=self.person_type_patient,
            department='test department',
            email='test@gmail.com',
            mzu_id='123456',
            is_active=True,
            mobile_no=1234567890
        )
        self.doctor = Person.objects.create(
            name='Test Doctor',
            person_type=self.person_type_doctor,
            department='test department',
            email='doctor@gmail.com',
            mzu_id='1234561212',
            is_active=True,
            mobile_no=1234567890
        )
        
        # Define prescription data with nested structures
        self.prescription_data_for_create = {
            'patient': self.patient.id,
            'doctor': self.doctor.id,
            'note': 'test note',
            'date_and_time': '10-12-2023 14:20:00',
            'prescription_dispense_status': Prescription.PresciptionDispenseStatus.NOT_DISPENSED,
            'prescribed_item_set': [
                {
                    'name': 'Test Medicine 1',
                    'item': self.item_1.id,
                    'dosages': [
                        {
                            'duration_value': 7,
                            'duration_type': 'days',
                            'note': 'Take once daily',
                            'medicine_dosage_timing_set': [
                                {
                                    'quantity_in_one_take': 1,
                                    'day_med_schedule': 'morning',
                                    'medicine_timing': 'before meal'
                                }
                            ]
                        }
                    ]
                },
                {
                    'name': 'Test Medicine 2',
                    'item': self.item_2.id,
                    'dosages': [
                        {
                            'duration_value': 14,
                            'duration_type': 'days',
                            'note': 'Take twice daily',
                            'medicine_dosage_timing_set': [
                                {
                                    'quantity_in_one_take': 1,
                                    'day_med_schedule': 'morning',
                                    'medicine_timing': 'after meal'
                                },
                                {
                                    'quantity_in_one_take': 1,
                                    'day_med_schedule': 'evening',
                                    'medicine_timing': 'after meal'
                                }
                            ]
                        }
                    ]
                }
            ]
        }

    def test_prescription_create(self):
        serializer = PrescriptionSerializer(data=self.prescription_data_for_create)
        if serializer.is_valid():
            serializer.save()
            # print_json_string(serializer.data)  # Uncomment to view serialized output
        else:
            print('---------------------------------ERRORS----------------------')
            print(serializer.errors)
            print('---------------------------------')

        self.assertEqual(Prescription.objects.count(), 1, "Check that one prescription is created")

    def test_prescription_view(self):
        serializer = PrescriptionSerializer(data=self.prescription_data_for_create)
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)

        prescription = Prescription.objects.first()
        serializer = PrescriptionSerializer(prescription)
        # print_json_string(serializer.data)  # Uncomment to view serialized output

