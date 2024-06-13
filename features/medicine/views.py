
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from features.medicine.models import MedicineDosage
from features.medicine.serializers import   MedicineDosageSerializer, MedicineSerializer
import django_filters.rest_framework

from rest_framework import generics
from .models import Item


# Create your views here.

class StandardResultsSetPagination(PageNumberPagination):
    """Standard pagination settings for the API results."""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class MedicineDosageViewSet(viewsets.ModelViewSet):
    queryset = MedicineDosage.objects.all()
    serializer_class = MedicineDosageSerializer



# class MedicineListView(generics.ListAPIView):
#     serializer_class = MedicineSerializer

#     def get_queryset(self):
#         return Item.objects.filter(type__category__name='Medicine')

# class MedicineDetailView(generics.RetrieveAPIView):
#     serializer_class = MedicineSerializer

#     def get_queryset(self):
#         return Item.objects.filter(type__category__name='Medicine')
    
class MedicineFilter(django_filters.FilterSet):
    item_id = django_filters.CharFilter(field_name='id', lookup_expr='icontains')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    type = django_filters.CharFilter(field_name='type__name', lookup_expr='icontains')
   
    class Meta:
        model = Item
        fields = ['item_id', 'name','type']

class MedicineViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.filter(type__category__name='Medicine')
    serializer_class = MedicineSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = MedicineFilter
    pagination_class = StandardResultsSetPagination
    # permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = [TokenAuthentication]