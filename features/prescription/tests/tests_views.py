from django.utils import timezone
import datetime
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from features.base.base_test_setup_class import BaseTestCase
from features.item.models import Item
from features.person.models import Department, Person, PersonType
from features.prescription.models import PrescriptionItem, Prescription
from features.prescription.serializers import PrescriptionSerializer


class PrescriptionViewSetTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        Person.objects.all().delete()
        Prescription.objects.all().delete()
        PrescriptionItem.objects.all().delete()
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
            mobile_no=1234567890
        )
        self.patient_2 = Person.objects.create(
            name='Test Patient 2',
            person_type=self.person_type_patient,
            department=self.department,
            email='test@gmail.com',
            mzu_id='1234565',
            is_active=True,
            mobile_no=1234567880
        )
        self.doctor_1 = Person.objects.create(
            name='Test Doctor 1',
            person_type=self.person_type_doctor,
            department=self.department,
            email='doctor1@gmail.com',
            mzu_id='1234561212',
            is_active=True,
            mobile_no=1234567890
        )

        self.doctor_2 = Person.objects.create(
            name='Test Doctor 2',
            person_type=self.person_type_doctor,
            department=self.department,
            email='doctor2@gmail.com',
            mzu_id='2234561212',
            is_active=True,
            mobile_no=1234567890
        )
       
        self.prescription_data_1 = {
            'patient': self.patient_1.id,
            'doctor': self.doctor_1.id,
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
        }# Create a few Prescription instances here
        
        
        self.prescription_data_2 = {
            'patient': self.patient_2.id,
            'doctor': self.doctor_2.id,
            'note': 'test note',
            'date_and_time': '20-1-2024 14:20:00',
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
        }# Create a few Prescription instances here
       
       

    def test_filter_prescription_view(self):
   
        url = reverse('prescription-list')
        
        self.client.post(url, self.prescription_data_1, format='json')
         
        self.client.post(url, self.prescription_data_2, format='json')

        # Test filtering by an exact date
        response = self.client.get(url, {'issue_date': '10-12-2023'})
        prescription=Prescription.objects.first()
       
        # # ------Filter by patient_id
        # response = self.client.get(url, {'patient_id': prescription.patient.id})
        # print("Expected patient ID:", prescription.patient.id)
        # print("Number of records returned:", len(response.data))
      
        # for item in response.data:
        #     print("\nReturned patient ID:", item['patient']['id'])
        #     print(item)  # Assuming patient ID is returned in the response
        #     print('\n---------\n')

        # ------filter by Mzu id
        print('\n')
        response = self.client.get(url, {'patient_mzu_id': prescription.patient.mzu_id})
        print("Expected patient mzu ID:", prescription.patient.mzu_id)
        print("Number of records returned:", len(response.data))
        print(response.data)

        # print('\n')
        # prescription2=Prescription.objects.last()
        # response = self.client.get(url, {'patient_mzu_id': prescription2.patient.mzu_id})
        # print("Expected patient mzu ID:", prescription2.patient.mzu_id)
        # print("Number of records returned:", len(response.data))
        # print(response.data)

        # # ---Filter by doctor_id
        # response = self.client.get(url, {'doctor_id': prescription.doctor.id})
        # print("Expected doctor ID:", prescription.doctor.id)
        # print("Number of records returned:", len(response.data))
        

        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # # Check if the length is not what's expected
        # self.assertEqual(len(response.data), 1, f"Expected 1 record, got {len(response.data)}")
      
       
        # # Additional checks to validate the contents of the response
        # self.assertEqual(response.data[0]['patient']['id'], str(self.prescription.patient.id))
        #      # ------Filter by patient_id
    #     response = self.client.get(url, {'doctor_id':prescription.doctor.id})
    #     # print_json_string(response.data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data), 1)
    #     self.assertEqual(response.data[0]['doctor']['id'], str(prescription.doctor.id))
     
    #     # -----Filter by date----
    #     response = self.client.get(url, {'date':'28-12-2022'})
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data),1)
        
    #     date_and_time_received=response.data[0]['date_and_time']
   
    #     self.assertEqual(date_and_time_received,self.date_and_time_1 )

    #     # # Test filtering by a range of dates
    #     response = self.client.get(url, {'date_from': '1-01-2023', 'date_to': '31-12-2023'})
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data), 1)
    #     date_and_time_received=response.data[0]['date_and_time']
    #     self.assertEqual(date_and_time_received,self.date_and_time_2 )

