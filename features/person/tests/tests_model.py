from django.test import TestCase

from datetime import date

from features.person.models import Patient, Person, PersonType

class PersonModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.person_type = PersonType.objects.create(
            name="Staff",
            description="University staff",
            abbreviation="STF"
        )

    def test_date_conversion_valid_date(self):
        # Testing valid date conversion
        person = Person.create(
            name="John Doe",
            email="john.doe@example.com",
            mzu_id="123456",
            date_of_birth="12-12-1970",  # DD-MM-YYYY format
            person_type=self.person_type
        )
        self.assertEqual(person.date_of_birth, date(1970, 12, 12))

    def test_date_conversion_invalid_date(self):
        # Testing invalid date string handling
        with self.assertRaises(ValueError):
            Person.create(
                name="Jane Doe",
                email="jane.doe@example.com",
                mzu_id="654321",
                date_of_birth="30-30-1970", 
                
                person_type=self.person_type
            )

    def test_unique_mzu_id(self):
        # Ensure mzu_id is unique
        Person.create(
            name="Alice Smith",
            email="alice.smith@example.com",
            mzu_id="999999",
            date_of_birth="15-06-1985",
            person_type=self.person_type
        )
        with self.assertRaises(Exception):  # Expecting IntegrityError but Django wraps this in Exception during tests
            Person.create(
                name="Bob Smith",
                email="bob.smith@example.com",
                mzu_id="999999",  # Duplicate mzu_id
                date_of_birth="16-06-1985",
                person_type=self.person_type
            )

    def test_person_type_relationship(self):
        # Testing ForeignKey relationship
        person = Person.create(
            name="Charles Brown",
            email="charles.brown@example.com",
            mzu_id="333333",
            date_of_birth="01-01-1980",
            person_type=self.person_type
        )
        self.assertEqual(person.person_type.name, "Staff")

    def test_model_field_defaults(self):
        # Testing the defaults of JSON fields in the derived Patient model
        patient = Patient.create(
            name="Diana Prince",
            email="diana.prince@example.com",
            mzu_id="777777",
            date_of_birth="20-07-1980",
            person_type=self.person_type
        )
        self.assertEqual(patient.allergy, [])
        self.assertEqual(patient.illness, [])

# Note: This test assumes that full_clean() in create will raise ValueError on invalid data, which is true if DateConverter is adjusted to do so.
