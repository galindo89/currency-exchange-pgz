"""
This file is used to configure the users app.
"""

from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    This class is used to configure the users app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
