
from features.inventory_transaction.dispense_transaction.models import DispenseInventoryTransaction
from features.inventory_transaction.dispense_transaction.serializers import DispenseInventoryTransactionSerializer
from features.inventory_transaction.dispense_transaction.tests.generate_dispense_transaction_data import generate_dispense_transaction_data
from features.inventory_transaction.dispense_transaction.tests.setup_indent_for_test import setup_indent_for_test
from features.inventory_transaction.dispense_transaction.tests.setup_prescription_for_test import setup_prescription_for_test


from features.base.base_test_setup_class import BaseTestCase



class DispenseInventoryTransactionSerializerTestCase(BaseTestCase):
    def setUp(self):
        print('-------Setup starting------')
        super().setUp()
        
  
        self.indent_transaction=setup_indent_for_test(self.item_type,self.unit_of_measurement,)
        
        
        self.prescription=setup_prescription_for_test(self.indent_transaction['medicine'])




    def test_create_dispense_transaction(self):
        DispenseInventoryTransaction.objects.all().delete()
        self.dispense_transaction_data=generate_dispense_transaction_data(self.prescription)
        # print(self.dispense_transaction_data)
        serializer=DispenseInventoryTransactionSerializer(data=self.dispense_transaction_data)
        if (serializer.is_valid()):
            serializer.save()
            print('Dispense serializer is valid')
            # return serializer.data
        else:
            print('Dispense Serializer is not valid')
            print(serializer.errors)