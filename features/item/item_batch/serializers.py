from rest_framework import serializers
from .models import ItemBatch

class ItemBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemBatch
        fields = ['batch_id', 'description', 'date_of_expiry', 'item', 'is_active', 'created_on', 'updated_on']