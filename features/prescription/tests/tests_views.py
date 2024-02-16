from django.utils import timezone
import datetime
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from features.base.base_test_setup_class import BaseTestCase
from features.item.models import Item
from features.person.models import Department, Person, PersonType
from features.prescription.models import PrescribedMedicine, Prescription
from features.prescription.serializers import PrescriptionSerializer
from features.utils.print_json import print_json_string

class PrescriptionViewSetTestCase(BaseTestCase):
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
        self.patient_1 = Person.objects.create(
            name='Test Patient 1',
            person_type=self.person_type_patient,
            department=self.department,
            email='test1@gmail.com',
            mzu_id='1234569',
            is_active=True,
            contact_no=1234567890
        )
        self.patient_2 = Person.objects.create(
            name='Test Patient 2',
            person_type=self.person_type_patient,
            department=self.department,
            email='test@gmail.com',
            mzu_id='1234565',
            is_active=True,
            contact_no=1234567880
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
        self.prescription_data_1 = {
            'patient': self.patient_1.id,
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
         }# Create a few Prescription instances here
        
        self.prescription_data_2 = {
            'patient': self.patient_2.id,
            'doctor': self.doctor.id,
            'note':'test note 2',
            'prescription_date':prescription_date,
            'prescription_dispense_status': Prescription.PressciptionDispenseStatus.NOT_DISPENSED,
            'prescribed_medicine_set': [
                {
                    'name': 'Test Medicine 1',
                    'dosage': 'Test Dosage 1',
                    'item': self.item_1.id
                },
                {
                    'name': 'Test Medicine 3',
                    'dosage': 'Test Dosage 3',
                    'item': self.item_2.id
                }
            ]
         }#

        # serialized_prescription = PrescriptionSerializer(data=self.prescription_data_1)
        # if serialized_prescription.is_valid():
        #     serialized_prescription.save()
        # else:
        #     print(serialized_prescription.errors)

        # serialized_prescription = PrescriptionSerializer(data=self.prescription_data_2)
        # if serialized_prescription.is_valid():
        #     serialized_prescription.save()
        # else:
        #     print(serialized_prescription.errors)

    # def tearDown(self):
    #     # Delete the Prescription instances here


    def test_filter_prescription_view(self):
   
        url = reverse('prescription-list')
        
        self.client.post(url, self.prescription_data_1, format='json')
        self.client.post(url, self.prescription_data_2, format='json')

        # Test filtering by an exact date
        # response = self.client.get(url, {'issue_date': '2022-01-01'})
        prescription=Prescription.objects.first()
        print("patient_id: ", prescription.patient.id)
      
        response = self.client.get(url, {'patient_id':prescription.patient.id})
        print_json_string(response.data)
     
        
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(len(response.data),1)
        # self.assertEqual(response.data[0]['issue_date'], '2022-01-01')

        # # # Test filtering by a range of dates
        # response = self.client.get(url, {'issue_date_from': '2022-01-01', 'issue_date_to': '2022-04-01'})
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(len(response.data), 1)

        #  # Test filtering by a range of dates
        # response = self.client.get(url, {'issue_date_from': '2022-02-01', 'issue_date_to': '2022-06-01'})
     
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(len(response.data), 1)