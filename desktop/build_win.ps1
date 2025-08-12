param(
  [string]$AppName = "TallerPG",
  [string]$Entry = "run_server.py"
)

$ErrorActionPreference = "Stop"

# Ensure venv active with PyInstaller installed
if (-not (Get-Command pyinstaller -ErrorAction SilentlyContinue)) {
  Write-Host "PyInstaller no encontrado. Activá el venv e instalá: pip install pyinstaller waitress reportlab" -ForegroundColor Yellow
  exit 1
}

# Clean previous builds
Remove-Item -Recurse -Force dist, build -ErrorAction SilentlyContinue | Out-Null

# Collect data files (templates)
$templates = "templates;templates"

# Build
pyinstaller --noconfirm --clean `
  --name $AppName `
  --onefile `
  --add-data $templates `
  --collect-all reportlab `
  --collect-all xhtml2pdf `
  --hidden-import reportlab.graphics.barcode.code128 `
  --hidden-import reportlab.graphics.barcode.eanbc `
  --hidden-import reportlab.graphics.barcode.usps `
  --hidden-import reportlab.graphics.barcode.pdf417 `
  --hidden-import reportlab.graphics.barcode.qr `
  $Entry

Write-Host "Build listo en dist\$AppName.exe" -ForegroundColor Green