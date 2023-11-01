from django.apps import AppConfig


class InstacloneConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'instaclone'

    def ready(self) -> None:
        import instaclone.signals