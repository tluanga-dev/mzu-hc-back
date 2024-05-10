import os
from django.core.wsgi import get_wsgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = 'your_project.settings'
application = get_wsgi_application()

from faker import Faker
from features.person.models import Employee, EmployeeDependent, Student

fake = Faker()

def create_employees(n):
    employees = []
    for _ in range(n):
        employee = Employee.objects.create(
            name=fake.name(),
            gender=fake.random_element(elements=('Male', 'Female', 'Other')),
            date_of_birth=fake.date_of_birth(),
            mobile_no=fake.random_number(digits=10),
            email=fake.email(),
            employee_type=fake.random_element(elements=('Employee', 'Employee Dependent', 'Student')),
            mzu_employee_id=fake.unique.random_number(digits=8),
            designation=fake.job()
        )
        employees.append(employee)
    return employees

def create_employee_dependents(employees):
    for _ in range(20):
        EmployeeDependent.objects.create(
            name=fake.name(),
            relation=fake.random_element(elements=('Son', 'Daughter', 'Spouse')),
            date_of_birth=fake.date_of_birth(),
            employee=fake.random_element(elements=employees)
        )

def create_students(n):
    for _ in range(n):
        Student.objects.create(
            name=fake.name(),
            gender=fake.random_element(elements=('Male', 'Female', 'Other')),
            date_of_birth=fake.date_of_birth(),
            department=fake.random_element(elements=('Engineering', 'Business', 'Literature')),
            mobile_no=fake.random_number(digits=10),
            email=fake.email(),
            mzu_student_id=fake.unique.random_number(digits=8)
        )

# Create mock data



def insertPersonObjectToDataBase():
    employees = create_employees(10)  # Adjust as necessary
    employee_dependent=create_employee_dependents(employees)
    students=create_students(20)
    # ---Insert into the database---
    Employee.objects.bulk_create(employees)

    EmployeeDependent.objects.bulk_create(employee_dependent)

    Student.objects.bulk_create(students)