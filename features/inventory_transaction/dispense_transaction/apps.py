from django.apps import AppConfig


class DispenseTransactionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "features.inventory_transaction.dispense_transaction"

    def ready(self):
        import features.inventory_transaction.dispense_transaction.signals