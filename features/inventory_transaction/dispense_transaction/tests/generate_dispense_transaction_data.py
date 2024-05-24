
from features.item.models import Item
from features.prescription.models import Prescription



def generate_dispense_transaction_data(prescription: Prescription):
    print(prescription)
    dispense_item_set = []

    if(not prescription):
        print(prescription)
        return None
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

