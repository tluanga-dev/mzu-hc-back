import logging
from django.core.management import BaseCommand, call_command
from django.db import transaction
from faker import Faker
from features.organisation_unit.models import OrganisationUnit
from features.person.models import Employee, EmployeeDependent, MZUOutsider, Student

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Populates the database with mock data'

    def handle(self, *args, **options):
        fake = Faker()

        @transaction.atomic
        def create_organisation_units(n):
            """Creates n organisation units."""
            organisation_units = []
            for _ in range(n):
                organisation_unit = OrganisationUnit(
                    name=fake.company(),
                    description=fake.sentence(),
                    abbreviation=fake.lexify('???')
                )
                organisation_units.append(organisation_unit)
            OrganisationUnit.objects.bulk_create(organisation_units)
            logger.info(f'Created {n} organisation units')
            return organisation_units

        @transaction.atomic
        def create_employees(n, organisation_units):
            """Creates n employees."""
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

        @transaction.atomic
        def create_employee_dependents(n, employees):
            """Creates n employee dependents."""
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

        @transaction.atomic
        def create_students(n, organisation_units):
            """Creates n students."""
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
                        programme=fake.random_element(elements=('MSc', 'MA', 'MBA')),
                        year_of_admission=fake.year()
                    )
                    students.append(student)
                except Exception as e:
                    logger.error(f'Error creating student: {e}')
            Student.objects.bulk_create(students)
            logger.info(f'Created {n} students')
            return students
        
        @transaction.atomic
        def create_mzu_outsider(n):
            """Creates n mzu outsider."""
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
                    logger.error(f'Error creating student: {e}')
            MZUOutsider.objects.bulk_create(mzu_outsiders)
            logger.info(f'Created {n} mzu outsider')
            return mzu_outsiders

        try:
            # Run the migrations
            logger.info('Running migrations')
            call_command('start_migrations')

            # Create mock data
            logger.info('Creating mock data')
            organisation_units = create_organisation_units(30)
            employees = create_employees(1000, organisation_units)
            create_employee_dependents(30000, employees)
            create_students(40000, organisation_units)
            create_mzu_outsider(10000)

            self.stdout.write(self.style.SUCCESS('Successfully populated the database with mock data'))
        except Exception as e:
            logger.error(f'Error populating database: {e}')
            self.stdout.write(self.style.ERROR('Error populating the database'))
