param(
  [switch]$NoRun
)

$ErrorActionPreference = "Stop"

Write-Host "== Taller Mecánico | Setup Windows ==" -ForegroundColor Cyan

# 1) Ir a la raíz del repo (si se ejecuta desde otra carpeta)
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Resolve-Path (Join-Path $scriptDir "..")
Set-Location $repoRoot

# 2) Políticas de ejecución
try {
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force | Out-Null
} catch {}

# 3) Crear/activar venv
if (-not (Test-Path .venv)) {
  Write-Host "Creando entorno virtual (.venv)..." -ForegroundColor Yellow
  py -m venv .venv
}
$venvActivate = Join-Path (Resolve-Path ".venv") "Scripts/Activate.ps1"
. $venvActivate

# 4) Pip y deps
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# 5) Variables de entorno para esta sesión
$env:USE_SQLITE = "true"
$env:DJANGO_SETTINGS_MODULE = "backend.settings"

# 6) Migraciones y static
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# 7) Seeds
python manage.py seed_roles
python manage.py seed_customers_perms
python manage.py seed_workorders_perms
python manage.py seed_inventory_perms
python manage.py seed_billing_perms

# 8) Superusuario por variables o defaults
$adminUser = if ($env:ADMIN_USERNAME) { $env:ADMIN_USERNAME } else { "admin" }
$adminEmail = if ($env:ADMIN_EMAIL) { $env:ADMIN_EMAIL } else { "admin@example.com" }
$adminPass = if ($env:ADMIN_PASSWORD) { $env:ADMIN_PASSWORD } else { "admin123" }

python manage.py shell -c "from django.contrib.auth import get_user_model; U=get_user_model();
import os; user='$adminUser'; email='$adminEmail'; pwd='$adminPass';
U.objects.filter(username=user).exists() or U.objects.create_superuser(user,email,pwd)"

if (-not $NoRun) {
  Write-Host "Iniciando servidor en http://127.0.0.1:8000/ (admin en /admin/)" -ForegroundColor Green
  python manage.py runserver 0.0.0.0:8000
} else {
  Write-Host "Setup completado. Ejecutá: .\.venv\Scripts\Activate.ps1 ; $env:USE_SQLITE='true' ; python manage.py runserver 0.0.0.0:8000" -ForegroundColor Green
}