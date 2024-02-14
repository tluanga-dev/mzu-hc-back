import json
from rest_framework import serializers

from features.base.base_test_setup_class import BaseTestCase
from features.person.models import Department, Person, PersonType
from features.person.serializers import PersonSerializer

class TestPersonSerializer(BaseTestCase):
    def setUp(self):
        super().setUp()
        Person.objects.all().delete()
        PersonType.objects.all().delete()
        Department.objects.all().delete()
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

        self.person_data={
            'name':'Test First Name',
            'person_type':self.person_type.id,
            'department':self.department.id,
            'email':'test@gmail.com',
            'mzu_id':'123456',
            'is_active':True,
            'contact_no':1234567890
        }
     

        


    def test_person_create_serializer(self):
        # print(self.person_data)
        serializer=PersonSerializer(data=self.person_data)
        if(serializer.is_valid()):
            serializer.save()
        else:
            print(serializer.errors)
        print(serializer.data)
    
        person=Person.objects.get(name=self.person_data['name'])
        self.assertEqual(person.name,self.person_data['name'])
        
        self.assertEqual(person.person_type.id,self.person_data['person_type'])
        self.assertEqual(person.department.id,self.person_data['department'])
        self.assertEqual(person.email,self.person_data['email'])
        self.assertEqual(person.mzu_id,self.person_data['mzu_id'])
        self.assertEqual(person.is_active,self.person_data['is_active'])
        self.assertEqual(person.contact_no,self.person_data['contact_no'])



    def test_retrieve_person_serializer(self):
        serializer=PersonSerializer(data=self.person_data)
        if(serializer.is_valid()):
            serializer.save()
        else:
            print(serializer.errors)
        person=Person.objects.get(name=self.person_data['name'])
        serializer=PersonSerializer(person)
        expected_data=self.person_data.copy()

        expected_data['person_type']={
            'id':self.person_type.id,
            'name':'Test Person Type',
            'description':'Test Description',
            'is_active':True
        }
        expected_data['department']={
            'id':self.department.id,
            'name':'Test Department',
            'description':'Test Description',
            'is_active':True
        }
        expected_data["id"]=person.id

        serializer.data["department"].pop('created_on', None)
        serializer.data["department"].pop('updated_on', None)
        serializer.data["person_type"].pop('created_on', None)
        serializer.data["person_type"].pop('updated_on', None)
        # serializer.data.pop('updated_on', None)
        print('serializer data',json.dumps(serializer.data, indent=4))
        print('expected data',json.dumps(expected_data, indent=4))
       
        self.assertEqual(serializer.data,expected_data)