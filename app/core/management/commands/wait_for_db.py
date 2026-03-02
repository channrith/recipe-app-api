"""Django command to wait for the database to be available."""

import time

from psycopg2 import OperationalError as Psycopg2OpError
from django.core.management.base import BaseCommand
from django.db.utils import OperationalError


class Command(BaseCommand):
    """Wait for the database to be ready before proceeding."""

    def add_arguments(self, parser):
        parser.add_argument(
            "--sleep",
            type=float,
            default=1,
            help="Seconds to wait between connection attempts (default: 1).",
        )
        parser.add_argument(
            "--max-attempts",
            type=int,
            default=30,
            help="Maximum number of connection attempts (default: 30).",
        )

    def handle(self, *args, **options):
        """Entrypoint for command."""

        self.stdout.write("Waiting for database...")

        sleep_secs = options["sleep"]
        max_attempts = options["max_attempts"]

        for attempt in range(1, max_attempts + 1):
            try:
                self.check(databases=["default"])
                self.stdout.write(self.style.SUCCESS("Database available!"))
                return
            except (Psycopg2OpError, OperationalError):
                self.stdout.write(
                    f"Database unavailable, retrying... ({attempt}/{max_attempts})"
                )
                if attempt < max_attempts:
                    time.sleep(sleep_secs)
                else:
                    raise
