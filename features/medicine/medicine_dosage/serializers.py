from rest_framework import serializers
from .models import MedicineDosage

class MedicineDosageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineDosage
        fields = ['id', 'quantity_in_one_take', 'how_many_times_in_a_day', 'name', 'item', 'updated_on']