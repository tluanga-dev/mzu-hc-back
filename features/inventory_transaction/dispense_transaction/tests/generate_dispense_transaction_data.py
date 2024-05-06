
from features.item.models import Item
from features.prescription.models import Prescription
from features.prescription.serializers import PrescriptionSerializer


def generate_dispense_transaction_data(prescription: Prescription):
    
    dispense_item_set = []
    for item in prescription['prescribed_item_set']:
        dispense_item_set.append({
            'item_id': item['medicine']['id'],
            'quantity': 1
        })

    
    return {
        'prescription': prescription['id'],
        'pharmacist': 'U Rsa',
        'dispense_item_set': dispense_item_set
    }

