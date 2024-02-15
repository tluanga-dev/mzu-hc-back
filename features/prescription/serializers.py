from rest_framework import serializers
from features.person.models import Department, Person
from features.person.serializers import PersonSerializer

from features.prescription.models import Prescription, PrescribedMedicine

class PrescribedMedicineSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PrescribedMedicine
        fields = [
            "__all__"
        ]

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['name']


class PrescriptionPersonSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['department'] = instance.department.name
        return representation

    class Meta:
        model = Person
        fields = ['name', 'department']


class PrescriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Prescription
        fields = [
            'code', 
            'patient', 
            'doctor', 
            'note', 
            'prescription_date',
            'prescription_dispense_status'
        ]
        read_only_fields = ['code']

    def to_representation(self, instance):
        self.fields['patient'] = PrescriptionPersonSerializer(read_only=True)
        self.fields['doctor'] = PrescriptionPersonSerializer(read_only=True)
        return super(PrescriptionSerializer, self).to_representation(instance)
    


 