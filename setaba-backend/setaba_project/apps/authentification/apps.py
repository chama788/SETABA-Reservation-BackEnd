from django.apps import AppConfig


class AuthentificationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.authentification'
    verbose_name = 'Authentification'

    def ready(self):
        # Import signals pour s'assurer qu'ils sont chargés
        # après que l'application soit prête
        import apps.authentification.signals
