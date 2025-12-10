"""
Custom management command to run the development server with different configurations.

Usage:
    python manage.py run dev   # Run in development mode (no HTTPS required)
    python manage.py run prod  # Run in production mode (HTTPS required)

This command uses separate settings modules:
    - dev mode: f1betting.settings.development
    - prod mode: f1betting.settings.production
"""

import os
import sys

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Run the development server in dev or prod mode"

    def add_arguments(self, parser):
        parser.add_argument(
            "mode",
            type=str,
            choices=["dev", "prod"],
            help="Server mode: 'dev' for development (no HTTPS) or 'prod' for production (HTTPS required)",
        )
        parser.add_argument(
            "addrport",
            nargs="?",
            default="8000",
            help="Optional port number or ipaddr:port (default: 8000)",
        )
        parser.add_argument(
            "--noreload",
            action="store_true",
            dest="noreload",
            default=False,
            help="Tells Django to NOT use the auto-reloader.",
        )

    def handle(self, *args, **options):
        mode = options["mode"]
        addrport = options["addrport"]
        noreload = options["noreload"]

        # Display banner based on mode
        if mode == "dev":
            self.stdout.write(self.style.SUCCESS("=" * 70))
            self.stdout.write(self.style.SUCCESS("🏎️  F1 Betting Pool - DEVELOPMENT MODE"))
            self.stdout.write(self.style.SUCCESS("=" * 70))
            self.stdout.write("")
            self.stdout.write(self.style.WARNING("Configuration:"))
            self.stdout.write("  • DEBUG = True")
            self.stdout.write("  • HTTPS/SSL = Disabled")
            self.stdout.write("  • Secure Cookies = Disabled")
            self.stdout.write("  • HSTS = Disabled")
            self.stdout.write("  • Email Backend = Console")
            self.stdout.write("  • Database = SQLite")
            self.stdout.write("")
            self.stdout.write(self.style.SUCCESS(f"✅ Starting server at http://localhost:{addrport}"))
            self.stdout.write(self.style.SUCCESS("   (no HTTPS required - perfect for your laptop!)"))
            self.stdout.write("")
            self.stdout.write(self.style.WARNING("⚠️  DO NOT USE IN PRODUCTION!"))
            self.stdout.write("=" * 70)
            self.stdout.write("")

            settings_module = "f1betting.settings.development"

        else:  # prod mode
            self.stdout.write(self.style.SUCCESS("=" * 70))
            self.stdout.write(self.style.SUCCESS("🏎️  F1 Betting Pool - PRODUCTION MODE"))
            self.stdout.write(self.style.SUCCESS("=" * 70))
            self.stdout.write("")
            self.stdout.write(self.style.WARNING("Configuration:"))
            self.stdout.write("  • DEBUG = False")
            self.stdout.write("  • HTTPS/SSL = Enabled")
            self.stdout.write("  • Secure Cookies = Enabled")
            self.stdout.write("  • HSTS = Enabled (1 year)")
            self.stdout.write("  • Security Headers = Enabled")
            self.stdout.write("")
            self.stdout.write(self.style.ERROR("🔒 HTTPS/SSL REQUIRED - HTTP will redirect to HTTPS"))
            self.stdout.write("")
            self.stdout.write(self.style.WARNING("⚠️  Make sure you have:"))
            self.stdout.write("  [ ] Strong SECRET_KEY set")
            self.stdout.write("  [ ] Proper ALLOWED_HOSTS configured")
            self.stdout.write("  [ ] Production database configured")
            self.stdout.write("  [ ] Email backend configured")
            self.stdout.write("  [ ] HTTPS certificates installed")
            self.stdout.write("=" * 70)
            self.stdout.write("")

            settings_module = "f1betting.settings.production"

        # Set the Django settings module
        os.environ["DJANGO_SETTINGS_MODULE"] = settings_module

        # Build the command to execute
        manage_py = sys.argv[0]
        cmd = [sys.executable, manage_py, "runserver", addrport]

        if noreload:
            cmd.append("--noreload")

        # Add the settings module
        cmd.extend(["--settings", settings_module])

        # Execute the runserver command with the appropriate settings
        try:
            os.execvp(sys.executable, cmd)
        except KeyboardInterrupt:
            self.stdout.write("")
            self.stdout.write(self.style.SUCCESS("\n👋 Server stopped. See you at the next race!"))
            sys.exit(0)
