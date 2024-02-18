
from googleapiclient.discovery import build
from features.item.models import ItemCategory, UnitOfMeasurement
from features.supplier.models import Supplier

from features.utils.print_json import print_json_string


    
sheet_id = '1Uj-SiWZVBiQnA4DkeQIO5Siwjvtzjl0wZ1_T_9bkrOo'
api_key='AIzaSyB9KRma3Pz2jc4dPa8F6C0raAcqWBV0cQM'

def authenticate():
    return build('sheets', 'v4', developerKey=api_key).spreadsheets()


def migrate_supplier():
    sheet_name='supplier'
    Supplier.objects.all().delete()
    sheets = authenticate()
    data=sheets.values().get(spreadsheetId=sheet_id, range=sheet_name).execute()
    print_json_string(data)
    
    for row in data['values'][1:]:
        print(row)
        Supplier.objects.create(
            name=row[1],
            abbreviation=row[2],
            contact_no=int(row[6]) if len(row) > 6 and row[6].isdigit() else 0,
            email=row[4],
            address=row[5],
            remarks=row[6] if len(row) > 6 else "",
        
        )
    print("Supplier migration complete")




def migrate_unit_of_measurement():
    sheet_name='unit_of_measurement'
    UnitOfMeasurement.objects.all().delete()
    sheets = authenticate()
    data=sheets.values().get(spreadsheetId=sheet_id, range=sheet_name).execute()
    for row in data['values'][1:]:
        UnitOfMeasurement.objects.create(
            name=row[1],
            abbreviation=row[2],
            description=row[3],
            example=row[4],
        )
    print("Unit of measurement migration complete")


def migrate_item_category():
    sheet_name='item_category'
    ItemCategory.objects.all().delete()
    sheets = authenticate()
    data=sheets.values().get(spreadsheetId=sheet_id, range=sheet_name).execute()
    for row in data['values'][1:]:
        ItemCategory.objects.create(
            name=row[1],
            abbreviation=row[2],
            description=row[3],
        
        )
    print("Item category migration complete")




def migrate():
    
    # Call the migrate method
    migrate_supplier()
    migrate_unit_of_measurement()
    migrate_item_category()

if __name__ == "__main__":
    migrate()
