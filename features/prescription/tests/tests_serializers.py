
from django.utils import timezone
import datetime
from features.base.base_test_setup_class import BaseTestCase
from features.item.models import Item
from features.person.models import Department, Person, PersonType
from features.person.serializers import PersonSerializer
from features.prescription.models import PrescribedMedicine, Prescription
from features.prescription.serializers import PrescriptionSerializer
from features.utils.print_json import print_json_string


class TestPresciption(BaseTestCase):
    def setUp(self):
        super().setUp()
        Person.objects.all().delete()
        Prescription.objects.all().delete()
        PrescribedMedicine.objects.all().delete()
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
        prescription_date = timezone.make_aware(datetime.datetime(2022, 12, 31, 23, 59, 59))
        self.prescription_data_for_create = {
            'patient': self.patient.id,
            'doctor': self.doctor.id,
            'note':'test note',
            'prescription_date':prescription_date,
            'prescription_dispense_status': Prescription.PressciptionDispenseStatus.NOT_DISPENSED,
            'prescribed_medicine_set': [
                {
                    'name': 'Test Medicine 1',
                    'dosage': 'Test Dosage 1',
                    'item': self.item_1.id
                },
                {
                    'name': 'Test Medicine 2',
                    'dosage': 'Test Dosage 2',
                    'item': self.item_2.id
                }
            ]
         }
        
    def tests_prescription_create(self):
        serializer=PrescriptionSerializer(data=self.prescription_data_for_create)
       
        if(serializer.is_valid()):
            serializer.save()
            print_json_string(serializer.data)  
        else:
            print('---------------------------------ERRORS----------------------')
            print(serializer.errors)
            print('---------------------------------')
        self.assertEqual(Prescription.objects.all().count(), 1)
       
    # def tests_prescription_view(self):
    #     serializer=PrescriptionSerializer(data=self.prescription_data_for_create)
    #     if(serializer.is_valid()):
            
    #         serializer.save()
    #     else:
    #         print(serializer.errors)
       
    #     prescription=Prescription.objects.first()
    #     serializer=PrescriptionSerializer(prescription)
        
    #     print_json_string(serializer.data)