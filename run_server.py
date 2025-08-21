import os
import time
import webbrowser
from pathlib import Path

os.environ.setdefault("USE_SQLITE", "true")
# Store DB in %APPDATA%\TallerPG\db.sqlite3 on Windows for persistence
appdata = os.getenv("APPDATA")
if appdata:
    data_dir = Path(appdata) / "TallerPG"
    data_dir.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("SQLITE_PATH", str(data_dir / "db.sqlite3"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

import django  # noqa: E402
from django.core.management import call_command  # noqa: E402
from waitress import serve  # noqa: E402

from backend.wsgi import application  # noqa: E402


def main() -> None:
    # Apply migrations
    call_command("migrate", interactive=False, verbosity=1)
    # Collect static for admin UI
    try:
        call_command("collectstatic", interactive=False, verbosity=0, clear=False, link=False)
    except Exception:
        pass
    # Seed base roles/permissions (best-effort)
    try:
        call_command("seed_roles")
        call_command("seed_customers_perms")
        call_command("seed_workorders_perms")
        call_command("seed_inventory_perms")
        call_command("seed_billing_perms")
    except Exception:
        pass
    host = os.getenv("APP_HOST", "127.0.0.1")
    port = int(os.getenv("APP_PORT", "8888"))
    url = f"http://{host}:{port}/admin/"
    # Open browser shortly after start
    if os.name == "nt":

        def _open():
            time.sleep(1.5)
            webbrowser.open(url)

        import threading

        threading.Thread(target=_open, daemon=True).start()
    print(f"Starting Taller PG at {url}")
    serve(application, host=host, port=port)


if __name__ == "__main__":
    django.setup()
    main()
