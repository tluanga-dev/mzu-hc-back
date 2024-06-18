
from googleapiclient.discovery import build
from features.id_manager.models import IdManager
from features.item.models import Item, ItemCategory, ItemType, UnitOfMeasurement
from features.organisation_unit.models import OrganisationUnit
from features.person.models import Person
from features.supplier.models import Supplier

import logging



from datetime import datetime

def convert_date_format(date_str):
    try:
        # Parse the date from dd-mm-yyyy
        date_obj = datetime.strptime(date_str, '%d-%m-%Y')
        # Convert it to yyyy-mm-dd format
        new_date_str = datetime.strftime(date_obj, '%Y-%m-%d')
        return new_date_str
    except ValueError:
        # Return the original input if it's not a valid date
        return date_str

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("migration_log.txt", mode='a'),
                        logging.StreamHandler()
                    ])

logger = logging.getLogger(__name__)

    
sheet_id = '1Uj-SiWZVBiQnA4DkeQIO5Siwjvtzjl0wZ1_T_9bkrOo'
api_key='AIzaSyB9KRma3Pz2jc4dPa8F6C0raAcqWBV0cQM'

def authenticate():
    return build('sheets', 'v4', developerKey=api_key).spreadsheets()

def migrate_supplier():
    sheet_name = 'supplier'
    Supplier.objects.all().delete()
    sheets = authenticate()
    data = sheets.values().get(spreadsheetId=sheet_id, range=sheet_name).execute()
    
    migrated_count = 0
    failed_count = 0

    for row in data['values'][1:]:
        try:
            Supplier.objects.create(
                name=row[1],
                abbreviation=row[2],
                contact_no=int(row[6]) if len(row) > 6 and row[6].isdigit() else 0,
                email=row[4],
                address=row[5],
                remarks=row[6] if len(row) > 6 else "",
            )
            migrated_count += 1
        except Exception as e:
            failed_count += 1
            logger.error(f"Failed to migrate supplier '{row[1]}': {e}")

    logger.info(f"Supplier migration complete. Migrated: {migrated_count}, Failed: {failed_count}")



def migrate_unit_of_measurement():
    sheet_name = 'unit_of_measurement'
    UnitOfMeasurement.objects.all().delete()
    sheets = authenticate()
    data = sheets.values().get(spreadsheetId=sheet_id, range=sheet_name).execute()

    migrated_count = 0
    failed_count = 0

    for row in data['values'][1:]:
        try:
            UnitOfMeasurement.objects.create(
                name=row[1],
                abbreviation=row[2],
                description=row[3],
                example=row[4],
            )
            migrated_count += 1
        except Exception as e:
            failed_count += 1
            logger.error(f"Failed to migrate unit of measurement '{row[1]}': {e}")

    logger.info(f"Unit of Measurement migration complete. Migrated: {migrated_count}, Failed: {failed_count}")


def migrate_item_category():
    sheet_name = 'item_category'
    ItemCategory.objects.all().delete()
    sheets = authenticate()
    data = sheets.values().get(spreadsheetId=sheet_id, range=sheet_name).execute()

    migrated_count = 0
    failed_count = 0

    for row in data['values'][1:]:
        try:
            ItemCategory.objects.create(
                name=row[1],
                abbreviation=row[2],
                description=row[3],
            )
            migrated_count += 1
        except Exception as e:
            failed_count += 1
            logger.error(f"Failed to migrate item category '{row[1]}': {e}")

    logger.info(f"Item Category migration complete. Migrated: {migrated_count}, Failed: {failed_count}")


def migrate_item_type():
    sheet_name = 'item_type'
    ItemType.objects.all().delete()
    sheets = authenticate()
    data = sheets.values().get(spreadsheetId=sheet_id, range=sheet_name).execute()

    migrated_count = 0
    failed_count = 0

    for row in data['values'][1:]:
        try:
            category = ItemCategory.objects.get(name=row[5])
            ItemType.objects.create(
                name=row[1],
                abbreviation=row[2],
                description=row[3],
                example=row[4],
                category=category
            )
            migrated_count += 1
        except Exception as e:
            failed_count += 1
            logger.error(f"Failed to migrate item type '{row[1]}': {e}")

    logger.info(f"Item Type migration complete. Migrated: {migrated_count}, Failed: {failed_count}")


def migrate_item():
    sheet_name = 'item'
    Item.objects.all().delete()
    sheets = authenticate()
    data = sheets.values().get(spreadsheetId=sheet_id, range=sheet_name).execute()

    migrated_count = 0
    failed_count = 0

    for row in data['values'][1:]:
        try:
            type = ItemType.objects.get(name=row[2])
            unit_of_measurement = UnitOfMeasurement.objects.get(name=row[3])
            is_consumable = row[4].lower() == 'true'
            contents = row[5] if len(row) > 5 and row[5] is not None else ''
            Item.objects.create(
                name=row[1],
                contents=contents,
                type=type,
                unit_of_measurement=unit_of_measurement,
                is_consumable=is_consumable,
                description='',
            )
            migrated_count += 1
        except Exception as e:
            failed_count += 1
            logger.error(f"Failed to migrate item '{row[1]}': {e}")

    logger.info(f"Item migration complete. Migrated: {migrated_count}, Failed: {failed_count}")


# def migrate_person_type():
#     sheet_name = 'person_type'
#     PersonType.objects.all().delete()
#     sheets = authenticate()
#     data = sheets.values().get(spreadsheetId=sheet_id, range=sheet_name).execute()

#     migrated_count = 0
#     failed_count = 0

#     for row in data['values'][1:]:
#         try:
#             PersonType.objects.create(
#                 name=row[1],
#                 abbreviation=row[2],
#                 description=row[3],
#             )
#             migrated_count += 1
#         except Exception as e:
#             failed_count += 1
#             logger.error(f"Failed to migrate person type '{row[1]}': {e}")

#     logger.info(f"Person Type migration complete. Migrated: {migrated_count}, Failed: {failed_count}")
def migrate_organisation_unit():
    sheet_name = 'organisation_unit'
    OrganisationUnit.objects.all().delete()
    sheets = authenticate()
    data = sheets.values().get(spreadsheetId=sheet_id, range=sheet_name).execute()

    migrated_count = 0
    failed_count = 0

    for row in data['values'][1:]:
        try:
            ItemCategory.objects.create(
                name=row[1],
                abbreviation=row[2],
                description=row[3],
            )
            migrated_count += 1
        except Exception as e:
            failed_count += 1
            logger.error(f"Failed to migrate item category '{row[1]}': {e}")

    logger.info(f"Item Category migration complete. Migrated: {migrated_count}, Failed: {failed_count}")


def migrate_person():
    sheet_name = 'person_nt'
    Person.objects.all().delete()
    sheets = authenticate()
    data = sheets.values().get(spreadsheetId=sheet_id, range=sheet_name).execute()

    migrated_count = 0
    failed_count = 0

    for row in data['values'][1:]:
        try:
            person_type = 'Non-Teaching'
            # date_of_birth=row[7],
            # print('\n----------------')
            # print('date of birth',date_of_birth)
            # print('-------\n')
            Person.objects.create(
                mzu_id=row[0],
                name=row[1],
                gender=row[2],
                email=row[3],
                mobile_no=int(row[4]) if len(row) > 3 and row[3].isdigit() else 0,
                department=row[5],
                designation=row[6],
                # date_of_birth='22-12-1970', --working
                date_of_birth=row[8],
                person_type=person_type
            )
            migrated_count += 1
        except Exception as e:
            failed_count += 1
            logger.error(f"Failed to migrate person '{row[1]}': {e}")

    logger.info(f"Person migration complete. Migrated: {migrated_count}, Failed: {failed_count}")



def migrate():
    
    # Call the migrate method
    IdManager.objects.all().delete()    
    migrate_supplier()
    migrate_unit_of_measurement()
    migrate_item_category()
    migrate_item_type()
    migrate_item()
    # migrate_person_type()
    migrate_person()
    

if __name__ == "__main__":
    migrate()