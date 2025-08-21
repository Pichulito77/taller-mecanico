from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Load infra/db/schema_v1.sql and schema_v2.sql into SQLite (USE_SQLITE=true)"

    def handle(self, *args, **options):
        engine = settings.DATABASES["default"]["ENGINE"]
        if not engine.endswith("sqlite3"):
            self.stdout.write("Not using SQLite; skipping.")
            return

        base_dir = Path(settings.BASE_DIR)
        schema_files = [
            base_dir / "infra" / "db" / "schema_v1.sql",
            base_dir / "infra" / "db" / "schema_v2.sql",
        ]

        with connection.cursor() as cursor:
            for path in schema_files:
                if not path.exists():
                    self.stdout.write(f"Schema file not found: {path}")
                    continue
                sql = path.read_text(encoding="utf-8")
                statements = [s.strip() for s in sql.split(";") if s.strip()]
                applied = 0
                for stmt in statements:
                    try:
                        cursor.execute(stmt)
                        applied += 1
                    except Exception as exc:  # idempotent: ignore already-exists kinds of errors
                        msg = str(exc).lower()
                        if "already exists" in msg or "duplicate" in msg:
                            continue
                        # Some engines may require IF NOT EXISTS; warn and continue
                        self.stdout.write(f"Warning executing: {stmt[:80]}... -> {exc}")
                self.stdout.write(self.style.SUCCESS(f"Applied {applied} statements from {path.name}"))

        self.stdout.write(self.style.SUCCESS("SQLite schema loaded."))