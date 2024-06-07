from rest_framework import serializers

from features.item.models import Item, ItemPackaging, MedicineDosageUnit
from features.item.serializers import ItemDetailSerializerForReport
from features.medicine.models import MedicineDosage, MedicineDosageTiming,  MedicineQuantityInOneTakeUnit

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


class ItemPackagingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPackaging
        fields = ['id', 'name', 'description', 'is_active', 'created_at', 'updated_at']


class MedicineDosageUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineDosageUnit
        fields = ['id', 'name', 'description','example','dosage_example', 'is_active', 'created_at', 'updated_at'
                  
                  ]

class MedicineSerializer(ItemDetailSerializerForReport):
   
    class Meta:
        model = Item 
        fields = '__all__'
            