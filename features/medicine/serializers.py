from rest_framework import serializers

from features.item.models import Item
from features.item.serializers import ItemDetailSerializerForReport
from features.medicine.models import MedicineDosage, MedicineDosageTiming, MedicineQuantityInOneTakeUnit

class MedicineQuantityInOneTakeUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineQuantityInOneTakeUnit
        fields = ['id', 'name']




    

class MedicineDosageTimingSerializer(serializers.ModelSerializer):
    medicine_dosage = serializers.PrimaryKeyRelatedField(
        read_only=True
    )
    class Meta:
        model = MedicineDosageTiming
        fields = [
            'id', 
            'quantity_in_one_take', 
            'day_med_schedule',
            'medicine_timing',
            'medicine_dosage',
            'updated_at'
        ]




class MedicineDosageSerializer(serializers.ModelSerializer):
    medicine_dosage_timing_set = MedicineDosageTimingSerializer(many=True)


    class Meta:
        model = MedicineDosage
        fields = ['duration_value', 'duration_type',  'medicine_dosage_timing_set']

    def create(self, validated_data):
        timings_data = validated_data.pop('medicine_dosage_timing_set', [])
        dosage = MedicineDosage.objects.create(**validated_data)
        for timing_data in timings_data:
            MedicineDosageTiming.objects.create(medicine_dosage=dosage, **timing_data)
        return dosage


class MedicineSerializer(ItemDetailSerializerForReport):
    # return the item details like name, description, type, unit_of_measurement
    # medicine_dosage = MedicineDosageSerializer(MedicineDosage, read_only=True)
    medicine_quantity_in_one_take_unit= MedicineQuantityInOneTakeUnitSerializer(many=True, read_only=True)



    class Meta:
        model = Item 
        fields = [
            'id', 'name', 'contents','description', 'type', 'unit_of_measurement','item_batches','quantity_in_stock',
              'medicine_quantity_in_one_take_unit']