// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'package:mzu_hc_manager/features/transaction/common/transaction_mode.dart';
import 'package:realm/realm.dart';

part 'schemas.g.dart';

// -------------------------------USER------------
@RealmModel()
class _UserType {
  @MapTo('_id')
  @PrimaryKey()
  late ObjectId id;
  late String name;
  late String abbreviation;
  late String description;
  late bool isActive;
  late DateTime createdOn;
  late DateTime updatedOn;

  @Backlink(#userType)
  late Iterable<_MZUSYSUser> users;
}

@RealmModel()
class _MZUSYSUser {
  @MapTo('_id')
  @PrimaryKey()
  late ObjectId id;
  // --userId
  // student-rollno
  // employee employee id
  // doctor and pharmacist- username
  late String mzuId;
  late String salutation;
  late String name;
  late String? shortenedName;
  late String description;
  late String? department;

  late String? address;
  late String? mobileNo;
  late String? emailAddress;
  late _UserType? userType;
  late bool isActive;
  late DateTime createdOn;
  late DateTime updatedOn;
}

// ---------------------------------ITEM------------------------------------------------

// -------------MASTER

@RealmModel()
class _ItemCategory {
  @MapTo('_id')
  @PrimaryKey()
  late ObjectId id;
  late String name;
  late String abbreviation;
  late String description;
  late bool isActive;
  late DateTime createdOn;
  late DateTime updatedOn;

  @Backlink(#category)
  late Iterable<_ItemType> types;
}

@RealmModel()
class _ItemType {
  @MapTo('_id')
  @PrimaryKey()
  late ObjectId id;
  late String name;
  late String abbreviation;
  late String description;
  late String example;
  late _ItemCategory? category;
  late bool isActive;
  late DateTime createdOn;
  late DateTime updatedOn;
}

@RealmModel()
class _UnitOfMeasurement {
  @MapTo('_id')
  @PrimaryKey()
  late ObjectId id;
  late String name;
  late String abbreviation;
  late String description;
  late String example;
  late bool isActive;
  late DateTime createdOn;
  late DateTime updatedOn;
}

// ---This will be updated every time there is a
// a transaction
@RealmModel()
class _ItemStockInfo {
  @MapTo('_id')
  @PrimaryKey()
  late ObjectId id;
  late int quantity;
  late _Item? item;
  late DateTime updatedOn;
}

@RealmModel()
class _MedicineDosage {
  @MapTo('_id')
  @PrimaryKey()
  late ObjectId id;
  late int quantityInOneTake;
  late int howManyTimesInAday;
  late String name;
  late List<_Item> item;
  late _MedicineDosageDuration? medicineDosage;
  late DateTime updatedOn;
}

@RealmModel()
class _MedicineDosageDuration {
  @MapTo('_id')
  @PrimaryKey()
  late ObjectId id;
  late int days;
  late String name;
  late _Item? item;
  late DateTime updatedOn;
}

@RealmModel()
class _Item {
  @MapTo('_id')
  @PrimaryKey()
  late ObjectId id;
  late String name;
  late String description;
  late _ItemType? type;
  late _UnitOfMeasurement? unitOfMeasurement;
  @Backlink(#item)
  late Iterable<_ItemBatch> batches;
  @Backlink(#item)
  late Iterable<_MedicineDosage> medicineDosage;
  @Backlink(#item)
  late Iterable<_MedicineDosageDuration> medicineDosageDuration;

  late _ItemStockInfo? itemStockInfo;

  late bool isActive;
  late DateTime createdOn;
  late DateTime updatedOn;
}

// --------Transaction
@RealmModel()
class _ItemBatch {
  @MapTo('_id')
  @PrimaryKey()
  late ObjectId id;
  late String batchId;
  late String description;
  late DateTime dateOfExpiry;
  late _Item? item;
  late bool isActive;
  
  late DateTime createdOn;
  late DateTime updatedOn;
}

// ----------------------------------------------------------------

// ----------------------------Office Department ----------------------------
// Equipment Recipient
// --------Transaction
@RealmModel()
class _Department {
  @MapTo('_id')
  @PrimaryKey()
  late ObjectId id;
  late String name;
  late String description;
  late bool isActive;
  late DateTime createdOn;
  late DateTime updatedOn;
}

// ----------------------------SUPPLIER ----------------------------
@RealmModel()
class _Supplier {
  @MapTo('_id')
  @PrimaryKey()
  late ObjectId id;
  late String name;
  late double contact;
  late String email;
  late String address;
  late String remarks;
  late bool isActive;
  late DateTime createdOn;
  late DateTime updatedOn;
}

// ----------------------------PERSON ----------------------------

@RealmModel()
class _Patient {
  @MapTo('_id')
  @PrimaryKey()
  late ObjectId id;
  late String patientId;
  late String name;
  late int mobileNumber;
  late String address;
  late String remarks;
  late String type;
  late _MZUSYSUser? mzuUserAccount;
  late bool isActive;
  late DateTime createdOn;
  late DateTime updatedOn;
}

// -------------------------------------------Transaction------------------------

@RealmModel()
class _TransactionItem {
  @MapTo('_id')
  @PrimaryKey()
  late ObjectId id;
  late _InventoryTransaction? inventoryTransaction;
  late int quantity;
  late _ItemBatch? batch;
  // this remarks can be use as precrtiption note in prescription
  late String remarks;
}

// ------Transaction type

@RealmModel()
class _IndentTransaction {
  @MapTo('_id')
  @PrimaryKey()
  late ObjectId id;
  late _InventoryTransaction? inventoryTransaction;
  late _Supplier? supplier;
  late String supplyOrderNo;
  late DateTime supplyOrderDate;
  late DateTime dateOfDeliverty;

  late String remarks;
  late bool isActive;
}

// Dispense medicine to patient
// a) with prescription
// b) without prescription - Person details needs to be entered
@RealmModel()
class _DispenseTransaction {
  @MapTo('_id')
  @PrimaryKey()
  late ObjectId id;
  late _InventoryTransaction? inventoryTransaction;
  late _Patient? patient;
  late String remarks;
  late _Prescription? prescription;
  late DateTime dateOfDispense;
  late DateTime createdOn;
  late DateTime updatedOn;
}

// Issue Item
// Issue item to office staff or department for official purpose only
@RealmModel()
class _MedicineIssueToDepartmentTransaction {
  @MapTo('_id')
  @PrimaryKey()
  late ObjectId id;
  late _InventoryTransaction? inventoryTransaction;
  late _Department? department;
  late String createdBy;
  late DateTime createdOn;
  late DateTime updatedOn;
}

// Returning Expiring Medicine to Supplier
// This will reduce the no of stocks in the inventory
@RealmModel()
class _MedicineReturnToSupplierTransaction {
  @MapTo('_id')
  @PrimaryKey()
  late ObjectId id;
  late _InventoryTransaction? inventoryTransaction;
  late _Supplier? supplier;
  late DateTime createdOn;
  late DateTime updatedOn;
}

// Returning Expiring Medicine to Supplier
// This will reduce the no of stocks in the inventory
@RealmModel()
class _MedicineReturnReplacementFromSupplierTransaction {
  @MapTo('_id')
  @PrimaryKey()
  late ObjectId id;
  late _InventoryTransaction? inventoryTransaction;
  late _Supplier? supplier;
  late DateTime createdOn;
  late DateTime updatedOn;
}

// ---Medicine that are to be dispose
@RealmModel()
class _MedicineDisposeTransaction {
  @MapTo('_id')
  @PrimaryKey()
  late ObjectId id;
  late _InventoryTransaction? inventoryTransaction;
  late String remarks;
  late DateTime createdOn;
  late DateTime updatedOn;
}

// ---End of Transaction Type

@RealmModel()
class _InventoryTransaction {
  @MapTo('_id')
  @PrimaryKey()
  late ObjectId id;
  late String transactionId;
  late String remarks;
  late DateTime createdOn;
  late DateTime modifiedOn;
  late String createdBy;
  late String transactionType;
  // ------transaction type---
  late _IndentTransaction? indentTransaction;
  late _DispenseTransaction? dispenseTransaction;
  late _MedicineReturnToSupplierTransaction?
      medicineReturnToSupplierTransaction;
  late _MedicineReturnReplacementFromSupplierTransaction?
      medicineReturnReplacementFromSupplierTransaction;
  late _MedicineDisposeTransaction? medicineDisposeTransaction;
  late _MedicineIssueToDepartmentTransaction?
      medicineIssueToDepartmentTransaction;

  @Backlink(#inventoryTransaction)
  late Iterable<_TransactionItem> transactionItems;
}

// -------Prescription---

@RealmModel()
class _Prescription {
  @MapTo('_id')
  @PrimaryKey()
  late ObjectId id;
  late String prescriptionId;
  late DateTime dateOfPrescription;
  late _Patient? patient;
  late String doctorsNote;
  late String status;
  late bool isActive;
  late List<_PrescribedMedicine> medicine;
  late _MZUSYSUser? doctor;
  late DateTime createdOn;
  late DateTime updatedOn;
}

@RealmModel()
class _PrescribedMedicine {
  @MapTo('_id')
  @PrimaryKey()
  late ObjectId id;
  late _Prescription? prescription;
  late _Item? item;
  late _MedicineDosage? medicineDosage;
  late String dosage;
  late String remarks;
}
