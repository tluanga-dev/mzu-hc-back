from rest_framework import serializers

from features.item.models import ItemCategory

class ItemCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCategory
        fields = ['id', 'name', 'abbreviation', 'description',
                  'is_active', 'created_at', 'updated_at']


class ItemCategorySerializerForUser(serializers.ModelSerializer):
    class Meta:
        model = ItemCategory
        fields = ['id', 'name', 'abbreviation', 'description']
