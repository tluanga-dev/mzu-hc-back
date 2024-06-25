from rest_framework import serializers
from features.inventory_transaction.inventory_transaction.models import ItemStockInfo
from features.item.models import Item, ItemPackaging, MedicineDosageUnit
from features.item.serializers.item_serializers import ItemDetailSerializerForReport
from features.medicine.models import MedicineDosage, MedicineDosageTiming, MedicineQuantityInOneTakeUnit

class MedicineQuantityInOneTakeUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineQuantityInOneTakeUnit
        fields = ['id', 'name']

class MedicineDosageTimingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineDosageTiming
        fields = [
            'id', 
            'quantity_in_one_take',
            'quantity_in_one_take_unit', 
            'day_med_schedule',
            'medicine_timing',
            'medicine_dosage',
            'updated_at'
        ]

class MedicineDosageSerializer(serializers.ModelSerializer):
    medicine_dosage_timing_set = MedicineDosageTimingSerializer(many=True)

    class Meta:
        model = MedicineDosage
        fields = ['duration_value', 'duration_type', 'note', 'medicine_dosage_timing_set']

    def create(self, validated_data):
        timings_data = validated_data.pop('medicine_dosage_timing_set', [])
        dosage = MedicineDosage.objects.create(**validated_data)
        for timing_data in timings_data:
            MedicineDosageTiming.objects.create(medicine_dosage=dosage, **timing_data)
        return dosage

class ItemPackagingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPackaging
        fields = [ 'name', 'unit',]

class MedicineDosageUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineDosageUnit
        fields = ['id', 'name', 'description', 'example', 'dosage_example']

class MedicineSerializer(serializers.ModelSerializer):
    dosage_unit = serializers.SerializerMethodField()
    packaging = serializers.SerializerMethodField()
    dosage = serializers.SerializerMethodField()
    dosage_timing = serializers.SerializerMethodField()
    
    def get_dosage_unit(self, instance):
        # Accessing the related MedicineDosageTiming through MedicineDosage
        dosage_units = MedicineDosageTiming.objects.filter(medicine_dosage__medicine=instance)
        if dosage_units.exists():
            return MedicineDosageUnitSerializer(dosage_units.first().quantity_in_one_take_unit).data
        return None

    def get_packaging(self, instance):
        # Assuming the Item model has a packaging field
        if instance.packaging:
            return ItemPackagingSerializer(instance.packaging).data
        return None

    def get_dosage(self, instance):
        dosages = MedicineDosage.objects.filter(medicine=instance)
        return MedicineDosageSerializer(dosages, many=True).data

    def get_dosage_timing(self, instance):
        dosage_timings = MedicineDosageTiming.objects.filter(medicine_dosage__medicine=instance)
        return MedicineDosageTimingSerializer(dosage_timings, many=True).data

    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'dosage_unit', 'packaging', 'dosage', 'dosage_timing']


class MedicineWithStockInfoSerializer(serializers.ModelSerializer):
    medicine_dosage_unit = MedicineDosageUnitSerializer(many=True, read_only=True)
    packaging = serializers.SerializerMethodField()
    dosage = serializers.SerializerMethodField()
    dosage_timing = serializers.SerializerMethodField()
    quantity_in_stock = serializers.IntegerField(read_only=True)
    type=serializers.CharField(source='type.name')


    def get_packaging(self, instance):
        if hasattr(instance, 'packaging'):
            return ItemPackagingSerializer(instance.packaging).data
        return None

    def get_dosage(self, instance):
        dosages = MedicineDosage.objects.filter(medicine=instance)
        return MedicineDosageSerializer(dosages, many=True).data

    def get_dosage_timing(self, instance):
        dosage_timings = MedicineDosageTiming.objects.filter(medicine_dosage__medicine=instance)
        return MedicineDosageTimingSerializer(dosage_timings, many=True).data

    def to_representation(self, instance):
        print("to_representation called")
        representation = super().to_representation(instance)
        item_stock_info = ItemStockInfo.objects.filter(item=instance).order_by('-updated_at').first()
        quantity_in_stock = item_stock_info.item_quantity_in_stock if item_stock_info else 0
        representation['quantity_in_stock'] = quantity_in_stock
        print(f"Item ID: {instance.id}, Quantity in Stock: {quantity_in_stock}")
        return representation

    class Meta:
        model = Item
        fields = ['id','type', 'name', 'contents', 'description', 'medicine_dosage_unit', 'packaging', 'dosage', 'dosage_timing','quantity_in_stock',]