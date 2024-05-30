import logging
from django.core.management import BaseCommand, call_command
from django.db import transaction
from faker import Faker
from features.inventory_transaction.indent_transaction.models import IndentInventoryTransaction
from features.organisation_unit.models import OrganisationUnit
from features.person.models import Employee, EmployeeDependent, MZUOutsider, Student
from features.patient.models import Patient
from features.prescription.models import Prescription, PrescriptionItem
from features.medicine.models import MedicineDosage, MedicineDosageTiming
from features.item.models import Item, ItemBatch, UnitOfMeasurement, ItemType, ItemCategory
from features.supplier.models import Supplier

logger = logging.getLogger(__name__)
fake = Faker()

class Command(BaseCommand):
    help = 'Populates the database with mock transaction data'

    def create_supplier(self, n):
        suppliers = []
        for _ in range(n):
            try:
                supplier = Supplier(
                    name=fake.company(),
                    abbreviation=fake.lexify('???'),
                    contact_no=fake.random_number(digits=10),
                    email=fake.email(),
                    address=fake.address(),
                    remarks=fake.sentence()
                )
                suppliers.append(supplier)
            except Exception as e:
                logger.error(f'Error creating supplier: {e}')
        Supplier.objects.bulk_create(suppliers)
        logger.info(f'Created {n} suppliers')
        return suppliers


    def create_indent_inventory_transaction(self, n, suppliers):
        indent_inventory_transactions = []
        for _ in range(n):
            try:
                indent_inventory_transaction = IndentInventoryTransaction(
                    supplier=fake.random_element(elements=suppliers),
                    supply_order_no=fake.random_element(
                        elements=['SO', 'PO', 'DO', 'RO', 'TO']
                    ) + str(fake.random_number(digits=6)),
                    supply_order_date=fake.date_this_year(),
                    date_of_delivery=fake.date_this_year()
                )
                indent_inventory_transactions.append(indent_inventory_transaction)
            except Exception as e:
                logger.error(f'Error creating indent inventory transaction: {e}')
        IndentInventoryTransaction.objects.bulk_create(indent_inventory_transactions)
        logger.info(f'Created {len(indent_inventory_transactions)} indent inventory transactions')
        return indent_inventory_transactions

    # def create_employees(self, n, organisation_units):
    #     employees = []
    #     for _ in range(n):
    #         try:
    #             employee = Employee(
    #                 name=fake.name(),
    #                 gender=fake.random_element(elements=('Male', 'Female', 'Other')),
    #                 date_of_birth=fake.date_of_birth(),
    #                 mobile_no=fake.random_number(digits=10),
    #                 employee_type=fake.random_element(elements=('Teaching', 'Non-Teaching')),
    #                 email=fake.email(),
    #                 organisation_unit=fake.random_element(elements=organisation_units),
    #                 mzu_employee_id=fake.unique.random_number(digits=8),
    #                 designation=fake.job()
    #             )
    #             employees.append(employee)
    #         except Exception as e:
    #             logger.error(f'Error creating employee: {e}')
    #     Employee.objects.bulk_create(employees)
    #     logger.info(f'Created {n} employees')
    #     return employees

    # def create_employee_dependents(self, n, employees):
    #     dependents = []
    #     for _ in range(n):
    #         try:
    #             dependent = EmployeeDependent(
    #                 mzu_employee_dependent_id=fake.lexify('????') + str(fake.random_number(digits=6)) + fake.lexify('???'),
    #                 name=fake.name(),
    #                 relation=fake.random_element(elements=('Son', 'Daughter', 'Spouse')),
    #                 date_of_birth=fake.date_of_birth(),
    #                 gender=fake.random_element(elements=('Male', 'Female', 'Other')),
    #                 employee=fake.random_element(elements=employees)
    #             )
    #             dependents.append(dependent)
    #         except Exception as e:
    #             logger.error(f'Error creating employee dependent: {e}')
    #     EmployeeDependent.objects.bulk_create(dependents)
    #     logger.info(f'Created {n} employee dependents')
    #     return dependents

    # def create_students(self, n, organisation_units):
    #     students = []
    #     for _ in range(n):
    #         try:
    #             student = Student(
    #                 name=fake.name(),
    #                 gender=fake.random_element(elements=('Male', 'Female', 'Other')),
    #                 date_of_birth=fake.date_of_birth(),
    #                 organisation_unit=fake.random_element(elements=organisation_units),
    #                 mobile_no=fake.random_number(digits=10),
    #                 email=fake.email(),
    #                 mzu_student_id=fake.unique.random_number(digits=8),
    #                 programme=fake.random_element(elements=('Msc', 'MA', 'MBA')),
    #                 year_of_admission=fake.year()
    #             )
    #             students.append(student)
    #         except Exception as e:
    #             logger.error(f'Error creating student: {e}')
    #     Student.objects.bulk_create(students)
    #     logger.info(f'Created {n} students')
    #     return students

    # def create_mzu_outsiders(self, n):
    #     mzu_outsiders = []
    #     for _ in range(n):
    #         try:
    #             mzu_outsider = MZUOutsider(
    #                 name=fake.name(),
    #                 gender=fake.random_element(elements=('Male', 'Female', 'Other')),
    #                 age=fake.random_int(min=18, max=100),
    #             )
    #             mzu_outsiders.append(mzu_outsider)
    #         except Exception as e:
    #             logger.error(f'Error creating MZU outsider: {e}')
    #     MZUOutsider.objects.bulk_create(mzu_outsiders)
    #     logger.info(f'Created {n} MZU outsiders')
    #     return mzu_outsiders

    # def create_patients(self, n, employees, students, dependents, outsiders):
    #     patients = []
    #     created_patients_info = []
    #     patient_lookup = {
    #         Patient.PatientType.EMPLOYEE: lambda: fake.random_element(elements=employees),
    #         Patient.PatientType.STUDENT: lambda: fake.random_element(elements=students),
    #         Patient.PatientType.EMPLOYEE_DEPENDENT: lambda: fake.random_element(elements=dependents),
    #         Patient.PatientType.MZU_OUTSIDER: lambda: fake.random_element(elements=outsiders)
    #     }

    #     attempts = 0
    #     max_attempts = n * 2  # To avoid infinite loops, set a reasonable upper limit on attempts

    #     while len(patients) < n and attempts < max_attempts:
    #         attempts += 1
    #         try:
    #             patient_type = fake.random_element(elements=[
    #                 Patient.PatientType.EMPLOYEE,
    #                 Patient.PatientType.STUDENT,
    #                 Patient.PatientType.EMPLOYEE_DEPENDENT,
    #                 Patient.PatientType.MZU_OUTSIDER
    #             ])

    #             related_entity = patient_lookup[patient_type]()

    #             with transaction.atomic():
    #                 if patient_type == Patient.PatientType.EMPLOYEE:
    #                     patient, created = Patient.objects.get_or_create(
    #                         employee=related_entity,
    #                         defaults={
    #                             'patient_type': Patient.PatientType.EMPLOYEE,
    #                             'illness': fake.sentence(),
    #                             'allergy': fake.sentence()
    #                         }
    #                     )
    #                 elif patient_type == Patient.PatientType.STUDENT:
    #                     patient, created = Patient.objects.get_or_create(
    #                         student=related_entity,
    #                         defaults={
    #                             'patient_type': Patient.PatientType.STUDENT,
    #                             'illness': fake.sentence(),
    #                             'allergy': fake.sentence()
    #                         }
    #                     )
    #                 elif patient_type == Patient.PatientType.EMPLOYEE_DEPENDENT:
    #                     patient, created = Patient.objects.get_or_create(
    #                         employee_dependent=related_entity,
    #                         defaults={
    #                             'patient_type': Patient.PatientType.EMPLOYEE_DEPENDENT,
    #                             'illness': fake.sentence(),
    #                             'allergy': fake.sentence()
    #                         }
    #                     )
    #                 elif patient_type == Patient.PatientType.MZU_OUTSIDER:
    #                     patient, created = Patient.objects.get_or_create(
    #                         mzu_outsider=related_entity,
    #                         defaults={
    #                             'patient_type': Patient.PatientType.MZU_OUTSIDER,
    #                             'illness': fake.sentence(),
    #                             'allergy': fake.sentence()
    #                         }
    #                     )

    #                 if created:
    #                     patients.append(patient)
    #                     created_patients_info.append({
    #                         'patient_id': patient.mzu_hc_id,
    #                         'patient_type': patient.get_patient_type_display(),
    #                         'related_entity': str(related_entity)
    #                     })

    #         except Exception as e:
    #             logger.error(f'Error creating patient: {e}')

    #     # if len(patients) < n:
    #     #     logger.warning(f'Only created {len(patients)} out of {n} patients after {attempts} attempts.')

    #     # for info in created_patients_info:
    #     #     print(f"Created patient with ID {info['patient_id']} of type {info['patient_type']} related to {info['related_entity']}")

    #     logger.info(f'Created {len(patients)} patients')
    #     return patients

    # def create_items(self, n):
    #     item_categories = [ItemCategory(name=fake.word(), abbreviation=fake.lexify('??'), description=fake.sentence()) for _ in range(5)]
    #     ItemCategory.objects.bulk_create(item_categories)

    #     item_types = [ItemType(name=fake.word(), abbreviation=fake.lexify('??'), description=fake.sentence(), category=fake.random_element(elements=item_categories)) for _ in range(5)]
    #     ItemType.objects.bulk_create(item_types)

    #     unit_of_measurements = [UnitOfMeasurement(name=fake.word(), abbreviation=fake.lexify('??'), description=fake.sentence(), example=fake.word()) for _ in range(5)]
    #     UnitOfMeasurement.objects.bulk_create(unit_of_measurements)

    #     items = []
    #     for _ in range(n):
    #         try:
    #             item = Item(
    #                 name=fake.word(),
    #                 contents=fake.text(),
    #                 item_code=fake.unique.lexify('??????'),
    #                 description=fake.text(),
    #                 type=fake.random_element(elements=item_types),
    #                 unit_of_measurement=fake.random_element(elements=unit_of_measurements),
    #                 is_consumable=fake.boolean()
    #             )
    #             items.append(item)
    #         except Exception as e:
    #             logger.error(f'Error creating item: {e}')
    #     Item.objects.bulk_create(items)
    #     logger.info(f'Created {n} items')
    #     return items

    # def create_prescriptions(self, n, patients):
    #     prescriptions = []
    #     for _ in range(n):
    #         try:
    #             patient = fake.random_element(elements=patients)
                
    #             prescription = Prescription(
    #                     patient=patient,
    #                     chief_complaints=fake.sentence(),
    #                     diagnosis=fake.sentence(),
    #                     advice_and_instructions=fake.sentence(),
    #                     note=fake.sentence(),
    #                     date_and_time=fake.date_time_this_year(),
    #                 )
               
    #             prescriptions.append(prescription)
    #         except Exception as e:
    #             logger.error(f'Error creating prescription: {e}')
    #     Prescription.objects.bulk_create(prescriptions)
    #     logger.info(f'Created {n} prescriptions')
    #     return prescriptions

    # def create_prescription_items(self, n, prescriptions, items):
    #     prescription_items = []
    #     for _ in range(n):
    #         try:
    #             prescription = fake.random_element(elements=prescriptions)
    #             item = fake.random_element(elements=items)
    #             prescription_item = PrescriptionItem(
    #                 prescription=prescription,
    #                 medicine=item,
    #                 note=fake.sentence()
    #             )
    #             prescription_items.append(prescription_item)
    #         except Exception as e:
    #             logger.error(f'Error creating prescription item: {e}')
    #     PrescriptionItem.objects.bulk_create(prescription_items)
    #     logger.info(f'Created {n} prescription items')
    #     return prescription_items

 
    def handle(self, *args, **kwargs):
        try:
            # Run the migrations
            logger.info('Running migrations')
            # call_command('start_migrations')
            call_command('populate_mock_data')
            # Create mock data
            logger.info('Creating mock data')
            suppliers = self.create_supplier(30)
            indent_transaction = self.create_indent_inventory_transaction(500, suppliers=suppliers)
            # dependents = self.create_employee_dependents(300, employees)
            # students = self.create_students(400, organisation_units)
            # outsiders = self.create_mzu_outsiders(200)
            # items = self.create_items(100)
            # patients = self.create_patients(1000, employees, students, dependents, outsiders)
            # prescriptions = self.create_prescriptions(10, patients)
            # self.create_prescription_items(15, prescriptions, items)

        except Exception as e:
            logger.error(f'Error populating database: {e}')
