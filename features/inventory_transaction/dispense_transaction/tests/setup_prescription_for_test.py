from features.organisation_unit.models import OrganisationUnit
from features.patient.models import Patient
from features.person.models import Employee, Person
from features.prescription.models import Prescription
from faker import Faker
from features.prescription.serializers.prescription_serializer import PrescriptionSerializer

def setup_prescription_for_test(medicine):
    # ---------Setup Prescription--------
    fake = Faker()
    patient_type = 'Employee'

    # Create and save OrganisationUnit instance
    organisation_unit = OrganisationUnit(
        name=fake.company(),
        description=fake.sentence(),
        abbreviation=fake.lexify('???')
    )
    organisation_unit.save()

    # Create and save Employee instance
    employee = Employee(
        name=fake.name(),
        gender=fake.random_element(elements=('Male', 'Female', 'Other')),
        date_of_birth=fake.date_of_birth(),
        mobile_no=fake.random_number(digits=10),
        employee_type=fake.random_element(elements=('Teaching', 'Non-Teaching')),
        email=fake.email(),
        organisation_unit=organisation_unit,
        mzu_employee_id=fake.unique.random_number(digits=8),
        designation=fake.job()
    )
    employee.save()

    # Create and save Patient instance
    patient = Patient(
        patient_type=patient_type,
        employee=employee,
        illness=fake.sentence(),
        allergy=fake.sentence()
    )
    patient.save()

    print('patient', patient)
    prescription_data = {
        "patient": patient.id,
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

    # Prescription.objects.all().delete()
    serializer = PrescriptionSerializer(data=prescription_data)

    if serializer.is_valid():
        print('serializer is valid')
        serializer.save()
        return serializer.data
    else:
        print('PrescriptionSerializer is not valid')
        print(serializer.errors)
