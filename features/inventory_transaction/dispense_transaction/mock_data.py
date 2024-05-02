# # step 1--this will be the input data received from the frontend
# inputData={
#     prescription_id: 1,
#     pharmacist: "Dr. John Doe",
#     dispense_item_set:[
#         {
#             item_id: 1,
#             quantity: 1
#         },
#          {
#             item_id: 2,
#             quantity: 100,
#         },
#     ]
# }
# # step 2- this input data will be processed by the serializer
# # using the helper function
# def find_batches_for_dispensing(item_id, required_quantity):
  
#     try:
#         item = Item.objects.get(id=item_id)
#     except Item.DoesNotExist:
#         print("Item not found")
#         return None

#     # Gather batches with available stock that hasn't expired, ordered by expiry date
#     batches = ItemBatch.objects.filter(
#         item=item,
#         quantity_in_stock__gt=0,  # Only consider batches with stock
#         date_of_expiry__gte=timezone.now().date()  # Exclude expired batches
#     ).order_by('date_of_expiry')

#     if not batches:
#         print("No available batches with stock found")
#         return None

#     dispense_list = []
#     total_dispensed = 0

#     # Iterate over batches to collect sufficient quantity
#     for batch in batches:
#         if total_dispensed >= required_quantity:
#             break
#         quantity_available_in_item_batch=ItemStockInfo.get_latest_by_item_batch_id(batch.id).quantity_in_stock
#         available_quantity = min(quantity_available_in_item_batch, required_quantity - total_dispensed)
#         dispense_list.append({
#             'item_batch': batch,
#             'quantity': available_quantity
#         })
#         total_dispensed += available_quantity

#     if total_dispensed < required_quantity:
#         print("Insufficient total stock to meet the requested quantity")

#     return {
#         'item': item,
#         'dispense_batches': dispense_list
#     }

#     # the manipulated resultant data to for the create method will be
#     modified_data={ prescription_id: 1,
#     pharmacist: "Dr. John Doe",
#         'inventory_transaction_item_set': dispense_list
#     }
#     this data will be processed by this serializer-class InventoryTransactionSerializer(serializers.ModelSerializer):
#     created_on = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")
#     updated_on = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S", read_only=True)

#     inventory_transaction_id = serializers.CharField(read_only=True)
#     inventory_transaction_item_set = serializers.ListSerializer(
#         child=InventoryTransactionItemSerializer(),
#         read_only=False
#     )
#     inventory_transaction_type=serializers.CharField(read_only=True)
#     created_on = serializers.SerializerMethodField()

#     def create(self, validated_data):
#         try:
#             transaction_items_data = validated_data.pop('inventory_transaction_item_set')
#             transaction = self.Meta.model.objects.create(**validated_data)
#             transaction.save()  # Ensure the transaction is saved
#             for transaction_item_data in transaction_items_data:
#                 InventoryTransactionItem.objects.create(inventory_transaction=transaction, **transaction_item_data)
#             return transaction
      
#         except ValueError as e:
#             print(f"ValueError: {e}")
#             raise serializers.ValidationError(str(e))
        
    
        
#     def update(self, instance, validated_data):
#         # Handle nested updates manually
#         transaction_items_data = validated_data.pop('inventory_transaction_item_set')
#         for item_data in transaction_items_data:
#             item_id = item_data.get('id', None)
#             if item_id:
#                 # Update existing items
#                 item = instance.inventory_transaction_item_set.get(id=item_id)
#                 for attr, value in item_data.items():
#                     setattr(item, attr, value)
#                 item.save()
#             else:
#                 # Create new items
#                 InventoryTransactionItem.objects.create(inventory_transaction=instance, **item_data)

#         # Update other fields normally
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         instance.save()

#         return instance
    
#     def get_created_on(self, obj):
#         return obj.created_on.strftime('%d-%m-%Y %H:%M')
    
