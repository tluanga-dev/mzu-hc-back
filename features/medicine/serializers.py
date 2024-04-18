from rest_framework import serializers

from features.medicine.models import MedicineDosage, MedicineDosageDuration


class MedicineDosageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineDosage
        fields = ['id', 'quantity_in_one_take', 'how_many_times_in_a_day', 'name', 'item', 'updated_on']


class MedicineDosageDurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineDosageDuration
        fields = ['id', 'days', 'name', 'medicine_dosage', 'updated_on']


