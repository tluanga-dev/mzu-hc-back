from features.inventory_transaction.inventory_transaction.serializers import InventoryTransactionSerializer
from features.inventory_transaction.issue_transaction.models import IssueItemInventoryTransaction
from features.organisation_section.serializers import OrganisationSectionSerializer


class IssueItemInventoryTransactionSerializer(InventoryTransactionSerializer):
   
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['issue_to'] = OrganisationSectionSerializer(instance.issue_to).data
        return representation
    
    class Meta:
        model = IssueItemInventoryTransaction
        fields = '__all__'