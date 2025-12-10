"""
Development settings for F1 Betting Pool.

This configuration is optimized for running on your local laptop without HTTPS.
Use with: python manage.py run dev
"""

from .base import *  # noqa

# Force development mode
DEBUG = True

# Allow localhost access (no wildcard for security)
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "testserver"]

# Use console email backend (prints emails to terminal)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# HTTPS/SSL settings are automatically disabled when DEBUG=True
# See base.py for the conditional security settings

# Development-friendly CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://localhost:8001",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8001",
]

# Enable Django Debug Toolbar if installed
try:
    import debug_toolbar  # noqa

    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE
    INTERNAL_IPS = ["127.0.0.1", "localhost"]
except ImportError:
    pass
