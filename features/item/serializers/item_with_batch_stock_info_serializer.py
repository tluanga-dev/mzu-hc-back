from rest_framework import serializers
from features.inventory_transaction.inventory_transaction.models import ItemStockInfo
from features.item.models import Item, ItemType, ItemBatch, UnitOfMeasurement, ItemPackaging, MedicineDosageUnit




class ItemDetailWithBatchStockInfoSerializer(serializers.ModelSerializer):
    quantity_in_stock = serializers.IntegerField(read_only=True)
    class Meta:
        model = Item
    

        fields = [
            'id', 'name', 'contents', 'description', 'type', 
            'unit_of_measurement', 'item_batches', 'quantity_in_stock',
            'packaging', 'medicine_dosage_unit'
        ]


    def to_representation(self, instance: Item) -> dict:
        """
        Custom representation of the item instance.
        """
        representation = super().to_representation(instance)

        item_stock_info = ItemStockInfo.get_latest_by_item_id(instance.id)
        quantity_in_stock = item_stock_info.item_quantity_in_stock if item_stock_info else 0
        representation['quantity_in_stock'] = quantity_in_stock
        # Manually include related data
        representation['type'] = {
            'id': instance.type.id,
            'name': instance.type.name,
        } if instance.type else None

        representation['unit_of_measurement'] = {
            'id': instance.unit_of_measurement.id,
            'abbreviation': instance.unit_of_measurement.abbreviation,
        } if instance.unit_of_measurement else None

        representation['packaging'] = {
            'id': instance.packaging.id,
            'name': instance.packaging.name,
        } if instance.packaging else None

        representation['medicine_dosage_unit'] = [
            {
                'id': unit.id,
                'name': unit.name,
            } for unit in instance.medicine_dosage_unit.all()
        ] if instance.medicine_dosage_unit.exists() else []

        representation['item_batches'] = [
            self.get_batch_representation(batch) for batch in instance.item_batches.all()
        ] if instance.item_batches.exists() else []

        return representation

    def get_batch_representation(self, batch: ItemBatch) -> dict:
        """
        Custom representation of each item batch, including the latest stock info.
        """
        batch_representation = {
            'id': batch.id,
            'batch_number': batch.batch_number,
            'expiry_date': batch.expiry_date,
            'quantity': batch.quantity,  # Default quantity
        }

        # Get the latest stock info for the batch
        latest_stock_info = ItemStockInfo.get_latest_stock_info_of_item_batch(batch.id)
        if latest_stock_info:
            batch_representation['quantity'] = latest_stock_info.quantity  # Update with the latest stock quantity

        return batch_representation
