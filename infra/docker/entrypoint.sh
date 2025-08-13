#!/usr/bin/env sh
set -e

# Wait for Postgres
if [ -n "$DATABASE_URL" ]; then
  echo "Waiting for database..."
  python - <<'PY'
import sys, time, os
import psycopg
from urllib.parse import urlparse
url = urlparse(os.environ['DATABASE_URL'])
for i in range(60):
    try:
        with psycopg.connect(os.environ['DATABASE_URL']) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT 1')
                print('Database is ready')
                sys.exit(0)
    except Exception as e:
        print('DB not ready yet...', e)
        time.sleep(1)
print('DB not ready after timeout')
sys.exit(1)
PY
fi

export DJANGO_SETTINGS_MODULE=backend.settings

python manage.py migrate --noinput
python manage.py collectstatic --noinput || true
# Best-effort seeds
python manage.py seed_roles || true
python manage.py seed_customers_perms || true
python manage.py seed_workorders_perms || true
python manage.py seed_inventory_perms || true
python manage.py seed_billing_perms || true

# Run server
exec python manage.py runserver 0.0.0.0:8000