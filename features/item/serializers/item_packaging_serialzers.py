from features.item.models import ItemPackaging
from rest_framework import serializers

class ItemPackagingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPackaging
        fields = ['id', 'name', 'label','unit', 'is_active']