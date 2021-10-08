"""File for Django apps configuration."""

from django.apps import AppConfig


class PollsConfig(AppConfig):
    """Class for polls app configuration."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'
