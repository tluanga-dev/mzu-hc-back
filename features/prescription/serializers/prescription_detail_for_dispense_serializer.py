from rest_framework import serializers

from features.inventory_transaction.inventory_transaction.models import ItemStockInfo
from features.prescription.models import Prescription, PrescriptionItem
from features.item.models import Item, ItemBatch
from features.medicine.serializers import MedicineDosageSerializer




class ItemSerializer(serializers.ModelSerializer):
    quantity_in_stock = serializers.SerializerMethodField()
    unit_of_measurement = serializers.CharField(source='unit_of_measurement.abbreviation', default=None)
    package_unit = serializers.CharField(source='packaging.name', default=None)

    def get_quantity_in_stock(self, obj):
        item_stock_info = ItemStockInfo.get_latest_by_item_id(obj.id)
        return 0 if item_stock_info is None else item_stock_info.item_quantity_in_stock

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Accessing only the name of the unit of measurement
        representation['item_with_batch_stock_infor'] = instance.unit_of_measurement.abbreviation if instance.unit_of_measurement else None
        representation['package_unit']=instance.packaging.name if instance.packaging else None
        return representation

    class Meta:
        model = Item
        fields = ['id', 'name', 'contents', 'unit_of_measurement', 'quantity_in_stock', 'package_unit']


class PrescriptionItemSerializer(serializers.ModelSerializer):
    dosages = MedicineDosageSerializer(many=True)
    medicine = ItemSerializer(source='item')

    class Meta:
        model = PrescriptionItem
        fields = ['id', 'note', 'dosages', 'medicine']




class PrescriptionDetailForDispenseSerializer(serializers.ModelSerializer):
    patient = serializers.SerializerMethodField()
    prescribed_item_set = PrescriptionItemSerializer(many=True, source='prescriptionitem_set')

    def get_patient(self, instance):
        patient = instance.patient
        return {
            'id': patient.id,
            'name': patient.get_name(),
            'patient_type': patient.patient_type,
            'mzu_id': patient.get_mzu_id(),
            'age': patient.get_age(),
            'gender': patient.get_gender(),
            'organisation_unit': patient.get_organisation_unit()
        }

    class Meta:
        model = Prescription
        fields = [
            'id', 'code', 'patient', 'chief_complaints', 'diagnosis',
            'advice_and_instructions', 'date_and_time', 'prescription_dispense_status',
            'prescribed_item_set'
        ]
        read_only_fields = ['id', 'code', 'patient', 'date_and_time', 'prescription_dispense_status']
