
from rest_framework import serializers

from features.setup.models import Setup

class SetupSerializer(serializers):
    class Meta:
        model = Setup
        fields = '__all__'

# class SetupSerializer(serializers.Serializer):
#     my_field = serializers.CharField(max_length=200)
#     my_integer_field = serializers.IntegerField()
