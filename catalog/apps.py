from django.apps import AppConfig


class CatalogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'catalog'
    verbose_name = "Каталог фильмов"

    def ready(self):
        import catalog.signals  # noqa: F401