from django.core.management.base import BaseCommand
from faker import Faker
from features.person.models import Employee, EmployeeDependent, Student  # Adjust the import path as necessary

class Command(BaseCommand):
    help = 'Populates the database with mock data'

    def handle(self, *args, **options):
        fake = Faker()

        def create_employees(n):
            employees = []
            for _ in range(n):
                employee = Employee(
                    name=fake.name(),
                    gender=fake.random_element(elements=('Male', 'Female', 'Other')),
                    date_of_birth=fake.date_of_birth(),
                    mobile_no=fake.random_number(digits=10),
                    employee_type=fake.random_element(elements=('Teaching', 'Non-Teaching' )),
                    email=fake.email(),
                    
                    department=fake.random_element(elements=('Administration', 'Examinations', 'Finance', 'Library', 'Registrar', 'Research', 'Student Affairs')),

                    mzu_employee_id=fake.unique.random_number(digits=8),
                    designation=fake.job()
                )
                employees.append(employee)
            return employees

        def create_employee_dependents(employees):
            dependents = []
            for _ in range(20):
                dependent = EmployeeDependent(
                    name=fake.name(),
                    relation=fake.random_element(elements=('Son', 'Daughter', 'Spouse')),
                    date_of_birth=fake.date_of_birth(),
                    employee=fake.random_element(elements=employees)
                )
                dependents.append(dependent)
            return dependents

        def create_students(n):
            students = []
            for _ in range(n):
                student = Student(
                    name=fake.name(),
                    gender=fake.random_element(elements=('Male', 'Female', 'Other')),
                    date_of_birth=fake.date_of_birth(),
                    department=fake.random_element(elements=('Engineering', 'Business', 'Literature')),
                    mobile_no=fake.random_number(digits=10),
                    email=fake.email(),
                    mzu_student_id=fake.unique.random_number(digits=8)
                )
                students.append(student)
            return students

        # Create mock data
        employees = create_employees(10)
        dependents = create_employee_dependents(employees)
        students = create_students(20)
    
        # -Clear previous data-
        Employee.objects.all().delete()
        EmployeeDependent.objects.all().delete()
        Student.objects.all().delete()

        # Insert into the database
        Employee.objects.bulk_create(employees)
        EmployeeDependent.objects.bulk_create(dependents)
        Student.objects.bulk_create(students)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with mock data'))
