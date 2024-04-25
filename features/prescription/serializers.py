from datetime import datetime
from rest_framework import serializers
from features.item.models import Item
from features.item.serializers import ItemSerializer
from features.medicine.models import MedicineDosage, MedicineDosageTiming
from features.medicine.serializers import MedicineDosageSerializer
from features.person.models import Department, Person
# from features.person.serializers import PersonSerializer
from django.utils.timezone import make_aware

from features.person.serializers import PersonSerializer
from features.prescription.models import Prescription, PrescriptionItem
from features.utils.convert_date import DateConverter
from django.db import transaction
from rest_framework import serializers
from datetime import datetime

from features.utils.print_json import print_json_string

class PrescribeMedicineItemSerializer(serializers.ModelSerializer):

  
    class Meta:
        model = Item
        fields = ['id', 'name','contents']

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
    
    
class PrescriptionDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id','name']


class PrescriptionPersonSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()

    def get_age(self, person):
        # Since date_of_birth is already a date object, we just use it directly
        date_of_birth = person.date_of_birth
        # Calculate the age based on today's date
        today = datetime.today().date()
        age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
        return age

    class Meta:
        model = Person
        fields = ['id','name','age','gender','person_type','designation', 'department','mzu_id']



class PrescriptionSerializer(serializers.ModelSerializer):
    prescribed_item_set = PrescriptionItemSerializer(many=True)
 
    date_and_time = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")


    class Meta:
        model = Prescription
        fields = [
            'id',
            'code', 
            'patient', 
            'doctor', 
            'chief_complaints',
            'diagnosis',
            'advice_and_instructions', 
            'date_and_time', 
            'prescription_dispense_status', 
            'prescribed_item_set'
        ]
        read_only_fields = ['code']

    @transaction.atomic
    def create(self, validated_data):
        # print(validated_data)
        prescribed_item_set_data = validated_data.pop('prescribed_item_set', [])

        prescription = Prescription.objects.create(**validated_data)
       
        for prescribed_item_data in prescribed_item_set_data:
            
            medicine_dosage_list_data = prescribed_item_data.pop('dosages', [])
           
            precription_item=PrescriptionItem.objects.create(**prescribed_item_data,prescription=prescription)
            medicine=precription_item.medicine
            for medicine_dosage_data in medicine_dosage_list_data:
                
                medicine_dosage_timing_set_data = medicine_dosage_data.pop('medicine_dosage_timing_set', [])
               
    
                medicine_dosage=MedicineDosage.objects.create(**medicine_dosage_data,medicine=medicine)
                precription_item.dosages.add(medicine_dosage)
                # -----Medicine Dosage Timing------
                for medicine_dosage_timing_data in medicine_dosage_timing_set_data:
                    medicine_dosage_timing = MedicineDosageTiming.objects.create(**medicine_dosage_timing_data,medicine_dosage=medicine_dosage)
                    medicine_dosage.medicine_dosage_timing_set.add(medicine_dosage_timing)

        return prescription

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['patient'] = PrescriptionPersonSerializer(instance.patient).data
        representation['doctor'] = PrescriptionPersonSerializer(instance.doctor).data
        return representation
  

    


 