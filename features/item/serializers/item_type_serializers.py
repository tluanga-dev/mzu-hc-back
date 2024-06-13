from rest_framework import serializers
from features.item.models import ItemType
from features.item.serializers.item_category_serializer import ItemCategorySerializerForUser


class ItemTypeSerializer(serializers.ModelSerializer):
    category = ItemCategorySerializerForUser(read_only=True)

    class Meta:
        model = ItemType
        fields = ['id', 'name', 'abbreviation', 'description',
                  'example', 'category', 'is_active', 'created_at', 'updated_at']


class ItemTypeSerializerForUser(serializers.ModelSerializer):
    category = ItemCategorySerializerForUser(read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = ItemCategorySerializerForUser(
            instance.category).data
        return representation

    class Meta:
        model = ItemType
        fields = ['id', 'name', 'abbreviation',
                  'description', 'example', 'category']