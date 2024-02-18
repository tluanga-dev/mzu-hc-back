from datetime import date
from django.test import TestCase
from django.urls import reverse

from features.base.base_test_setup_class import BaseTestCase
from features.inventory_transaction.indent_transaction.models import IndentInventoryTransaction
from features.inventory_transaction.indent_transaction.serializers import IndentInventoryTransactionSerializer
from features.inventory_transaction.inventory_transaction.models import InventoryTransaction, InventoryTransactionItem
from features.item.models import Item, ItemBatch
from features.person.models import Department, Person, PersonType
from features.person.serializers import PersonSerializer
from features.supplier.models import Supplier

class DispenseInventoryTransactionTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        Item.objects.all().delete()
        InventoryTransactionItem.objects.all().delete()
        IndentInventoryTransaction.objects.all().delete()
        ItemBatch.objects.all().delete()
        Supplier.objects.all().delete()
        Person.objects.all().delete()
        Department.objects.all().delete()
        PersonType.objects.all().delete()
        
        self.item = Item.objects.create(
            name="Test Item",
            description="Test Description",
            type=self.item_type,
            unit_of_measurement=self.unit_of_measurement,
            is_active=True
        )

        self.supplier = Supplier.objects.create(
            name='Test Supplier', 
            address='Test Address', 
            contact_no=1234567890,
            email='test@gmail.com'
        )
        self.item_batch = ItemBatch.objects.create(
            batch_id='B1',
            description='Test Batch 1',
            date_of_expiry=date.today(),
            item=self.item
        )
        self.person_student_type = PersonType.objects.create(
            name='Student Patient',
            description='Student Patient',
            is_active=True
        )

        self.person_doctor_type = PersonType.objects.create(
            name='Doctor',
            description='Doctor',
            is_active=True
        )
        self.department = Department.objects.create(
            name='Test Department',
            description='Test Description',
            is_active=True
        )

        self.patient = Person.objects.create(
            name='Test First Name',
            person_type=self.person_student_type,
            department=self.department,
            email='test@gmail.com',
            mzu_id='123456',
            is_active=True,
            contact_no=1234567890
        )

        self.doctor = Person.objects.create(
            name='dR. Test First Name',
            person_type=self.person_doctor_type,
            department=self.department,
            email='doc@gmail.com',
            mzu_id='mzunt_123',
            is_active=True,
            contact_no=1234567890
        )

        self.indent_transaction_data = {
                'inventory_transaction_type': InventoryTransaction.TransactionTypes.INDENT,
                'supplier': self.supplier.id,
                'supply_order_no': 'SO1',
                'supply_order_date': '2022-01-01',
                'date_of_delivery': '2022-01-01',
                'remarks': None,
                'inventory_transaction_item_set': [
                    {
                        'item_batch': self.item_batch.id,
                        'quantity': 1000,
                        'inventory_transaction_type': 'ITEM_INDENT',
                        'is_active': True
                    },
                    
                ]
            }
        IndentInventoryTransaction.objects.all().delete()
        serializer=IndentInventoryTransactionSerializer(data=self.indent_transaction_data)
       
        
        if(serializer.is_valid()):
            serializer.save()
            # print(serializer.data)
        else:
            print('serializer is not valid')
            print(serializer.errors)

        self.dispense_transaction_data_1= {
            'patient': str(self.patient.id),
            'doctor': str(self.doctor.id),
            'dispense_date': '01-01-2022',
            'inventory_transaction_item_set': [
                {
                    'item_batch': str(self.item_batch.id), 
                    'quantity': 500, 
                    'is_active': True
                },
            ],
            'inventory_transaction_type': 'dispense',
        }

        self.dispense_transaction_data_2= {
            'patient': str(self.patient.id),
            'doctor': str(self.doctor.id),
            'dispense_date': '01-01-2023',
            'inventory_transaction_item_set': [
                {
                    'item_batch': str(self.item_batch.id), 
                    'quantity': 100, 
                    'is_active': True
                },
            ],
            'inventory_transaction_type': 'dispense',
        }



    def test_dispense_inventory_transaction_creation(self):
        url = reverse('indent-inventory-transactions-list')  # Replace with the actual name of the URL
        # response = self.client.post(url, data, format='json')
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        

        print('test')

