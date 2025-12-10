"""
Django settings for f1betting project.

This file imports from the settings package for backward compatibility.
The actual settings are in f1betting/settings/base.py

For development mode, use: python manage.py run dev
For production mode, use: python manage.py run prod

For traditional runserver, copy .env.development to .env and use:
python manage.py runserver
"""

# Import all settings from the base module
from .settings.base import *  # noqa
