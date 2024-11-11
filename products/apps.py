# products/apps.py

from django.apps import AppConfig

class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'

    def ready(self):
        # Import the signals module to ensure it's loaded
        import products.signals
