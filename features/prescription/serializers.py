from rest_framework import serializers
from features.item.models import Item
from features.person.models import Department, Person
from features.person.serializers import PersonSerializer

from features.prescription.models import Prescription, PrescribedMedicine

class PrescribeMedicineItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name',]

class PrescribedMedicineSerializer(serializers.ModelSerializer):
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['item'] =PrescribeMedicineItemSerializer(instance.item).data
        return representation
    class Meta:
        model = PrescribedMedicine
        fields = [
           'id',
            'name',
            'dosage',
            'item'
        ]

class PrescriptionDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id','name']


class PrescriptionPersonSerializer(serializers.ModelSerializer):
    department = PrescriptionDepartmentSerializer(read_only=True)
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['department'] = PrescriptionDepartmentSerializer(instance.department).data
        return representation

    class Meta:
        model = Person
        fields = ['id','name', 'department']


class PrescriptionSerializer(serializers.ModelSerializer):

    prescribed_medicine_set = serializers.ListSerializer(
        child=PrescribedMedicineSerializer(),
        read_only=False
    )

    def create(self, validated_data):
        try:
            # print(f"validated_data: {validated_data}")
            items_data = validated_data.pop('prescribed_medicine_set')
            prescription = self.Meta.model.objects.create(**validated_data)
            
            for item_data in items_data:
                data=PrescribedMedicine.objects.create(prescription=prescription, **item_data)
                
            return prescription
      
        except ValueError as e:
            print(f"ValueError: {e}")
            raise serializers.ValidationError(str(e))

    
    class Meta:
        model = Prescription
        fields = [
            'code', 
            'patient', 
            'doctor', 
            'note', 
            'prescription_date',
            'prescription_dispense_status',
            'prescribed_medicine_set',
        ]
        read_only_fields = ['code']

    def to_representation(self, instance):
        self.fields['patient'] = PrescriptionPersonSerializer(read_only=True)
        self.fields['doctor'] = PrescriptionPersonSerializer(read_only=True)
        return super(PrescriptionSerializer, self).to_representation(instance)
    


 