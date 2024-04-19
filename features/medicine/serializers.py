from rest_framework import serializers

from features.medicine.models import MedicineDosage, MedicineDosageTiming


class MedicineDosageSerializer(serializers.ModelSerializer):
    medicine_dosage_element=serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset=MedicineDosageTiming.objects.all())
    class Meta:
        model = MedicineDosage
        fields = [
            'id', 
          'medicine_dosage_element',
            'medicine',
            'duration_value', 'duration_type', 
            'note'
              ]


class MedicineDosageTimingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineDosageTiming
        fields = [
            'id', 
            'quantity_in_one_take', 
            'dayMedSchedule',
            'medicineTiming'
            'medicine_dosage',
            'updated_on'
        ]


