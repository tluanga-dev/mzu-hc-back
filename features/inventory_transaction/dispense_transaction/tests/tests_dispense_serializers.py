from datetime import date
import json



from features.inventory_transaction.dispense_transaction.tests.setup_indent_for_test import setup_indent_for_test
from features.inventory_transaction.dispense_transaction.tests.setup_prescription_for_test import setup_prescription_for_test
from features.person.models import Person, PersonType
from features.prescription.models import Prescription
from features.prescription.serializers import PrescriptionSerializer
from features.utils.print_json import print_json_string
from features.utils.uuid_encoder import UUIDEncoder
from features.base.base_test_setup_class import BaseTestCase
from features.id_manager.models import IdManager
from features.inventory_transaction.indent_transaction.models import IndentInventoryTransaction
from features.inventory_transaction.indent_transaction.serializers import IndentInventoryTransactionSerializer
from features.inventory_transaction.inventory_transaction.models import InventoryTransaction, InventoryTransactionItem
from features.item.models import Item, ItemBatch


from features.supplier.models import Supplier


class DispenseInventoryTransactionSerializerTestCase(BaseTestCase):
    def setUp(self):
        print('-------Setup starting------')
        super().setUp()
        
  
        indent_transaction=setup_indent_for_test(self.item_type,self.unit_of_measurement,)
        

        prescription_data=setup_prescription_for_test(indent_transaction['medicine'])




    def test_create_dispense_transaction(self):
        print('\n-------test_create_prescription------- ')

    