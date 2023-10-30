from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ecom_apps.user'

    def ready(self):
        import ecom_apps.user.signals  # noqa
