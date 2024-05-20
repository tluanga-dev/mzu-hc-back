import logging
from django.core.management import BaseCommand, call_command
from django.db import transaction
from faker import Faker
from features.organisation_unit.models import OrganisationUnit
from features.person.models import Employee, EmployeeDependent, MZUOutsider, Student
from features.patient.models import Patient
from features.prescription.models import Prescription, PrescriptionItem
from features.medicine.models import MedicineDosage, MedicineDosageTiming
from features.item.models import Item, ItemBatch, UnitOfMeasurement, ItemType, ItemCategory

logger = logging.getLogger(__name__)
fake = Faker()

class Command(BaseCommand):
    help = 'Populates the database with mock data'

    def create_organisation_units(self, n):
        organisation_units = []
        for _ in range(n):
            try:
                organisation_unit = OrganisationUnit(
                    name=fake.company(),
                    description=fake.sentence(),
                    abbreviation=fake.lexify('???')
                )
                organisation_units.append(organisation_unit)
            except Exception as e:
                logger.error(f'Error creating organisation unit: {e}')
        OrganisationUnit.objects.bulk_create(organisation_units)
        logger.info(f'Created {n} organisation units')
        return organisation_units

    def create_employees(self, n, organisation_units):
        employees = []
        for _ in range(n):
            try:
                employee = Employee(
                    name=fake.name(),
                    gender=fake.random_element(elements=('Male', 'Female', 'Other')),
                    date_of_birth=fake.date_of_birth(),
                    mobile_no=fake.random_number(digits=10),
                    employee_type=fake.random_element(elements=('Teaching', 'Non-Teaching')),
                    email=fake.email(),
                    organisation_unit=fake.random_element(elements=organisation_units),
                    mzu_employee_id=fake.unique.random_number(digits=8),
                    designation=fake.job()
                )
                employees.append(employee)
            except Exception as e:
                logger.error(f'Error creating employee: {e}')
        Employee.objects.bulk_create(employees)
        logger.info(f'Created {n} employees')
        return employees

    def create_employee_dependents(self, n, employees):
        dependents = []
        for _ in range(n):
            try:
                dependent = EmployeeDependent(
                    mzu_employee_dependent_id=fake.lexify('????') + str(fake.random_number(digits=6)) + fake.lexify('???'),
                    name=fake.name(),
                    relation=fake.random_element(elements=('Son', 'Daughter', 'Spouse')),
                    date_of_birth=fake.date_of_birth(),
                    gender=fake.random_element(elements=('Male', 'Female', 'Other')),
                    employee=fake.random_element(elements=employees)
                )
                dependents.append(dependent)
            except Exception as e:
                logger.error(f'Error creating employee dependent: {e}')
        EmployeeDependent.objects.bulk_create(dependents)
        logger.info(f'Created {n} employee dependents')
        return dependents

    def create_students(self, n, organisation_units):
        students = []
        for _ in range(n):
            try:
                student = Student(
                    name=fake.name(),
                    gender=fake.random_element(elements=('Male', 'Female', 'Other')),
                    date_of_birth=fake.date_of_birth(),
                    organisation_unit=fake.random_element(elements=organisation_units),
                    mobile_no=fake.random_number(digits=10),
                    email=fake.email(),
                    mzu_student_id=fake.unique.random_number(digits=8),
                    programme=fake.random_element(elements=('Msc', 'MA', 'MBA')),
                    year_of_admission=fake.year()
                )
                students.append(student)
            except Exception as e:
                logger.error(f'Error creating student: {e}')
        Student.objects.bulk_create(students)
        logger.info(f'Created {n} students')
        return students

    def create_mzu_outsiders(self, n):
        mzu_outsiders = []
        for _ in range(n):
            try:
                mzu_outsider = MZUOutsider(
                    name=fake.name(),
                    gender=fake.random_element(elements=('Male', 'Female', 'Other')),
                    age=fake.random_int(min=18, max=100),
                )
                mzu_outsiders.append(mzu_outsider)
            except Exception as e:
                logger.error(f'Error creating MZU outsider: {e}')
        MZUOutsider.objects.bulk_create(mzu_outsiders)
        logger.info(f'Created {n} MZU outsiders')
        return mzu_outsiders

    def create_patients(self, n, employees, students, dependents, outsiders):
        patients = []
        for _ in range(n):
            try:
                patient_type = fake.random_element(elements=('Employee', 'Student', 'Employee Dependent', 'Other'))
                if patient_type == 'Employee':
                    employee = fake.random_element(elements=employees)
                    patient = Patient(
                        patient_type=patient_type,
                        employee=employee,
                        illness=fake.sentence(),
                        allergy=fake.sentence()
                    )
                elif patient_type == 'Student':
                    student = fake.random_element(elements=students)
                    patient = Patient(
                        patient_type=patient_type,
                        student=student,
                        illness=fake.sentence(),
                        allergy=fake.sentence()
                    )
                elif patient_type == 'Employee Dependent':
                    dependent = fake.random_element(elements=dependents)
                    patient = Patient(
                        patient_type=patient_type,
                        employee_dependent=dependent,
                        illness=fake.sentence(),
                        allergy=fake.sentence()
                    )
                else:
                    outsider = fake.random_element(elements=outsiders)
                    patient = Patient(
                        patient_type=patient_type,
                        mzu_outsider_patient=outsider,
                        illness=fake.sentence(),
                        allergy=fake.sentence()
                    )
                patients.append(patient)
            except Exception as e:
                logger.error(f'Error creating patient: {e}')
        Patient.objects.bulk_create(patients)
        logger.info(f'Created {n} patients')
        return patients

    def create_items(self, n):
        item_categories = [ItemCategory(name=fake.word(), abbreviation=fake.lexify('??'), description=fake.sentence()) for _ in range(5)]
        ItemCategory.objects.bulk_create(item_categories)

        item_types = [ItemType(name=fake.word(), abbreviation=fake.lexify('??'), description=fake.sentence(), category=fake.random_element(elements=item_categories)) for _ in range(5)]
        ItemType.objects.bulk_create(item_types)

        unit_of_measurements = [UnitOfMeasurement(name=fake.word(), abbreviation=fake.lexify('??'), description=fake.sentence(), example=fake.word()) for _ in range(5)]
        UnitOfMeasurement.objects.bulk_create(unit_of_measurements)

        items = []
        for _ in range(n):
            try:
                item = Item(
                    name=fake.word(),
                    contents=fake.text(),
                    item_code=fake.unique.lexify('??????'),
                    description=fake.text(),
                    type=fake.random_element(elements=item_types),
                    unit_of_measurement=fake.random_element(elements=unit_of_measurements),
                    is_consumable=fake.boolean()
                )
                items.append(item)
            except Exception as e:
                logger.error(f'Error creating item: {e}')
        Item.objects.bulk_create(items)
        logger.info(f'Created {n} items')
        return items

    def create_prescriptions(self, n, patients):
        prescriptions = []
        for _ in range(n):
            try:
                patient = fake.random_element(elements=patients)
                prescription = Prescription(
                    patient=patient,
                    chief_complaints=fake.sentence(),
                    diagnosis=fake.sentence(),
                    advice_and_instructions=fake.sentence(),
                    note=fake.sentence(),
                    date_and_time=fake.date_time_this_year(),
                )
                print('prescription_code', prescription.code)
                prescription.save()
                prescriptions.append(prescription)
            except Exception as e:
                logger.error(f'Error creating prescription: {e}')
        Prescription.objects.bulk_create(prescriptions)
        logger.info(f'Created {n} prescriptions')
        return prescriptions

    def create_prescription_items(self, n, prescriptions, items):
        prescription_items = []
        for _ in range(n):
            try:
                prescription = fake.random_element(elements=prescriptions)
                item = fake.random_element(elements=items)
                prescription_item = PrescriptionItem(
                    prescription=prescription,
                    medicine=item,
                    note=fake.sentence()
                )
                prescription_items.append(prescription_item)
            except Exception as e:
                logger.error(f'Error creating prescription item: {e}')
        PrescriptionItem.objects.bulk_create(prescription_items)
        logger.info(f'Created {n} prescription items')
        return prescription_items

 
    def handle(self, *args, **kwargs):
        try:
            # Run the migrations
            logger.info('Running migrations')
            call_command('start_migrations')

            # Create mock data
            logger.info('Creating mock data')
            organisation_units = self.create_organisation_units(30)
            employees = self.create_employees(10, organisation_units)
            dependents = self.create_employee_dependents(30, employees)
            students = self.create_students(40, organisation_units)
            outsiders = self.create_mzu_outsiders(10)
            patients = self.create_patients(50, employees, students, dependents, outsiders)
            items = self.create_items(10)
            prescriptions = self.create_prescriptions(5, patients)
            # self.create_prescription_items(15, prescriptions, items)

        except Exception as e:
            logger.error(f'Error populating database: {e}')
