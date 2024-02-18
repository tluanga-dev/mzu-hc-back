from datetime import date
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from features.base.base_test_setup_class import BaseTestCase
from features.inventory_transaction.indent_transaction.models import IndentInventoryTransaction
from features.inventory_transaction.indent_transaction.serializers import IndentInventoryTransactionSerializer
from features.inventory_transaction.inventory_transaction.models import InventoryTransaction, InventoryTransactionItem, ItemStockInfo
from features.item.models import Item, ItemBatch
from features.person.models import Department, Person, PersonType
from features.person.serializers import PersonSerializer
from features.prescription.models import Prescription
from features.prescription.serializers import PrescriptionSerializer
from features.supplier.models import Supplier

class DispenseInventoryTransactionTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        try:
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
            self.prescription=Prescription.objects.create(
                patient=self.patient,
                doctor=self.doctor,
                date_and_time='2021-01-01',
                prescription_dispense_status=Prescription.PresciptionDispenseStatus.NOT_DISPENSED,
                note='Test Note',
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
            serializer=IndentInventoryTransactionSerializer(data=self.indent_transaction_data)
            
            if(serializer.is_valid()):
                serializer.save()
                # print(serializer.data)
            else:
                print('serializer is not valid')
                print(serializer.errors)

        except ValueError as e:
            print(f"Error: {e}")

        self.dispense_transaction_data_1= {
            'patient': str(self.patient.id),
            'doctor': str(self.doctor.id),
            'dispense_date': '01-01-2022',
            'prescription': str(self.prescription.id),
            'inventory_transaction_item_set': [
                {
                    'item_batch': str(self.item_batch.id), 
                    'quantity': 500, 
                    'is_active': True
                },
            ],
            'inventory_transaction_type': 'dispense',
        }



    def test_dispense_inventory_transaction_creation(self):
        dispense_url = reverse('dispense-inventory-transactions-list')  # Replace with the actual name of the URL
        response = self.client.post(
            dispense_url, 
            self.dispense_transaction_data_1, 
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # --prescription data got updated--
        prescription=Prescription.objects.get(id=self.prescription.id)
        self.assertEqual(prescription.prescription_dispense_status, Prescription.PresciptionDispenseStatus.DISPENSED)

        # --item stock info got updated--
        item_stock_info=ItemStockInfo.objects.filter(item=self.item).last()
        print(item_stock_info.quantity)
