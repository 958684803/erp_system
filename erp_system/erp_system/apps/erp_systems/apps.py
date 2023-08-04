from django.apps import AppConfig


class ErpSystemsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "erp_systems"

    def ready(self):

        import erp_systems.signals
