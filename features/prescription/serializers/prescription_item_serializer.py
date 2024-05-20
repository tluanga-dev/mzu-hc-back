from rest_framework import serializers
from features.item.models import Item
from features.medicine.serializers import MedicineDosageSerializer
from features.prescription.models import PrescriptionItem
from features.prescription.serializers.prescriped_medicine_item_serializer import PrescribeMedicineItemSerializer


class PrescriptionItemSerializer(serializers.ModelSerializer):
    dosages = MedicineDosageSerializer(many=True)
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['medicine'] = PrescribeMedicineItemSerializer(instance.medicine).data
        return representation

    class Meta:
        model = PrescriptionItem
        fields = ['id', 'note', 'dosages', 'medicine']

    def create(self, validated_data):
        dosages_data = validated_data.pop('dosages', [])
        item_data = validated_data.pop('item')
        item = Item.objects.get(id=item_data['id'])  # Assuming existence or use ItemSerializer to create
        prescription_item = PrescriptionItem.objects.create(item=item, **validated_data)
        for dosage_data in dosages_data:
            dosage = MedicineDosageSerializer().create(dosage_data)
            prescription_item.dosages.add(dosage)
        return prescription_item