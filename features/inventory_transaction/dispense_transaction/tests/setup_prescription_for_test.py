from features.person.models import Person, PersonType
from features.prescription.models import Prescription
from features.prescription.serializers import PrescriptionSerializer


def setup_prescription_for_test(medicine):
    # ---------Setup Prescription--------
    PersonType.objects.all().delete()
    doctor_type = PersonType.objects.create(
            name='Doctor',
            description='A qualified practitioner of medicine; a physician.',
            abbreviation='DR'
        )

    # Create PersonType entry for 'Patient'
    patient_type = PersonType.objects.create(
            name='Patient',
            description='A person who is receiving medical treatment.',
            abbreviation='PT'
        )
    
    Person.objects.all().delete()
    patient = Person.create(
            name='John Doe',
            gender='Male',
            mzu_id='P001',
            date_of_birth='1985-04-23',
            department='General Medicine',
            designation='None',  # Patients do not have a designation
            person_type=patient_type,
            mobile_no=1234567890,
            email='john.doe@example.com'
    )

    doctor = Person.create(
            name='Dr. Sarah Smith',
            gender='Female',
            mzu_id='D001',
            date_of_birth='1970-06-15',
            department='Cardiology',
            designation='Senior Cardiologist',
            person_type=doctor_type,
            mobile_no=9876543210,
            email='sarah.smith@example.com'
        )

    prescription_data={
                "patient": patient.id,
                "doctor": doctor.id,
                "date_and_time": "02-05-2024 11:58:04",
                "chief_complaints": "this is the chief complain",
                "diagnosis": "this is the diagnosis",
                "advice_and_instructions": "this is the advice and instructions",
                "note": "",
                "prescribed_item_set": [
                    {
                        "medicine": medicine.id,
                        "dosages": [
                            {
                                "duration_value": 30,
                                "duration_type": "days",
                                "note": "",
                                "medicine_dosage_timing_set": [
                                    {
                                        "quantity_in_one_take": 1,
                                        "day_med_schedule": "Morning",
                                        "medicine_timing": "before_meal"
                                    },
                                    {
                                        "quantity_in_one_take": 1,
                                        "day_med_schedule": "Night",
                                        "medicine_timing": "after_meal"
                                    }
                                ]
                            },
                            {
                                "duration_value": 100,
                                "duration_type": "days",
                                "note": "",
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
    Prescription.objects.all().delete()
    serializer = PrescriptionSerializer(
            data=prescription_data)

    if (serializer.is_valid()):
        serializer.save()
       
        return serializer.data
    else:
        print('Prescriptionserializer is not valid')
        print(serializer.errors)
