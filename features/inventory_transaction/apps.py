from django.apps import AppConfig


class InventoryTransactionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "features.inventory_transaction"

    def ready(self):
        import features.inventory_transaction.signals
       