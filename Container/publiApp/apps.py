from django.apps import AppConfig


class PubliappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'publiApp'

    def ready(self):
        import publiApp.signals