from django.apps import AppConfig


class ItemConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "features.item"

    def ready(self):
        import features.item.signals

