from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from features.patient.models import Patient, Employee
from features.person.models import OrganisationUnit
from features.item.models import Item, UnitOfMeasurement
from features.medicine.models import MedicineDosage, MedicineDosageTiming
from faker import Faker

class PrescriptionViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.fake = Faker()
        
        # Set up organisation unit
        self.organisation_unit = OrganisationUnit.objects.create(
            name=self.fake.company(),
            description=self.fake.sentence(),
            abbreviation=self.fake.lexify('???')
        )

        # Set up employee
        self.employee = Employee.objects.create(
            name=self.fake.name(),
            gender=self.fake.random_element(elements=('Male', 'Female', 'Other')),
            date_of_birth=self.fake.date_of_birth(),
            mobile_no=self.fake.random_number(digits=10),
            employee_type=self.fake.random_element(elements=('Teaching', 'Non-Teaching')),
            email=self.fake.email(),
            organisation_unit=self.organisation_unit,
            mzu_employee_id=self.fake.unique.random_number(digits=8),
            designation=self.fake.job()
        )

        # Set up patient
        self.patient = Patient.objects.create(
            patient_type='Employee',
            employee=self.employee,
            illness=self.fake.sentence(),
            allergy=self.fake.sentence()
        )

        # Set up unit of measurement
        self.unit_of_measurement = UnitOfMeasurement.objects.create(
            abbreviation='mg',
            name='milligram'
        )

        # Set up item and medicine dosage
        self.item = Item.objects.create(
            name='Test Medicine', 
            contents='Test Content',
            unit_of_measurement=self.unit_of_measurement
        )

        self.medicine_dosage = MedicineDosage.objects.create(
            medicine=self.item,
            duration_value=30, 
            duration_type='days'
        )

        self.medicine_dosage_timing = MedicineDosageTiming.objects.create(
            quantity_in_one_take=1,
            day_med_schedule='Morning',
            medicine_timing='before_meal',
            medicine_dosage=self.medicine_dosage
        )

        # Prescription data for creation
        self.prescription_data = {
            "patient_type": "Employee",
            "patient_data": {
                # "id": self.patient.id,
                "patient_type": "Employee",
                "employee": self.employee.id  # Provide the employee ID
            },
            "prescription_data": {
                "chief_complaints": "Chief complaint",
                "diagnosis": "Diagnosis",
                "advice_and_instructions": "Advice",
                "date_and_time": "2024-05-22T11:58:04",  # ISO 8601 format
                "prescribed_item_set": [
                    {
                        "medicine": self.item.id,
                        "dosages": [
                            {
                                "duration_value": 30,
                                "duration_type": "days",
                                "medicine_dosage_timing_set": [
                                    {
                                        "quantity_in_one_take": 1,
                                        "day_med_schedule": "Morning",
                                        "medicine_timing": "before_meal"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        }

    def test_create_prescription(self):
        url = reverse('prescription-list')
        print(self.prescription_data)
        response = self.client.post(url, self.prescription_data, format='json')
        # print(response.status_code)
        print(response.data)  # Print response data to see the validation errors
        self.assertEqual(response.status_code, 201)
        self.assertIn('patient', response.data)
        self.assertIn('prescription', response.data)
