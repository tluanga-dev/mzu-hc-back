from django.test import TestCase

from features.person.models import Department, Person, PersonType
from features.person.serializers import PersonSerializer

class TestModels(TestCase):
    def setUp(self):
        # Set up non-modified objects used by all test methods
        Person.objects.all().delete()
        self.person_type = PersonType.objects.create(
            name='Test Person Type',
            description='Test Description',
            is_active=True
        )
        self.department = Department.objects.create(
            name='Test Department',
            description='Test Description',
            is_active=True
        )
        super().setUp()
    def test_person_creation(self):
        self.person = Person.objects.create(
            name='Test First Name',
            person_type=self.person_type,
            department=self.department,
            email='test@gmail.com',
            mzu_id='123456',
            is_active=True,
            contact_no=1234567890
        )
        # print(PersonSerializer(self.person).data)
        

        self.assertEqual(Person.objects.count(), 1)

    