from rest_framework import viewsets
from rest_framework.response import Response
from features.inventory_transaction.inventory_transaction.serializers import ItemTransactionDetailSerializer
from features.item.models import Item

    
class ItemTransactionsView(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemTransactionDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        print(f"Retrieving item with pk: {kwargs.get('pk')}")  # Print the PK to the console
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
