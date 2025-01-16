"""
App configuration for the Offers app.
"""
from django.apps import AppConfig


class OffersConfig(AppConfig):
    """
    Configures the Offers application within the Django project.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'offers'
