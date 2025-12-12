"""
Production settings for F1 Betting Pool.

This configuration enforces HTTPS/SSL and all security features.
Use with: python manage.py run prod
"""

import dj_database_url
from decouple import config
from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa

# Force production mode
DEBUG = False

# Production requires proper ALLOWED_HOSTS configuration
# Override with environment variable
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="").split(",")

if not ALLOWED_HOSTS or ALLOWED_HOSTS == [""]:
    raise ImproperlyConfigured(
        "ALLOWED_HOSTS must be set in production. " "Set the ALLOWED_HOSTS environment variable to your domain."
    )

# Force strong SECRET_KEY in production
SECRET_KEY = config("SECRET_KEY")
if SECRET_KEY.startswith("django-insecure-"):
    raise ImproperlyConfigured(
        "Cannot use default SECRET_KEY in production. "
        "Generate a secure key with: "
        'python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"'
    )

# Production email backend (must be configured)
EMAIL_BACKEND = config("EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend")

# Database configuration using DATABASE_URL
# Override default SQLite with PostgreSQL in production
DATABASE_URL = config("DATABASE_URL", default=None)
if DATABASE_URL:
    DATABASES["default"] = dj_database_url.parse(  # noqa: F405
        DATABASE_URL,
        conn_max_age=600,  # Connection pooling
        conn_health_checks=True,
    )

# CSRF trusted origins for proxied HTTPS deployments
# Required when using reverse proxy (nginx, load balancer, etc.)
CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS", default="").split(",")
CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in CSRF_TRUSTED_ORIGINS if origin.strip()]

# All HTTPS/SSL settings are automatically enabled when DEBUG=False
# See base.py for the conditional security settings
