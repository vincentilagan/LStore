# Publish LStore - one command to update the live store.
#
#   1. Drop your signed .vx into  apps\
#   2. Run:  .\publish.ps1 "add MyApp"
#
# It rebuilds apps.json from the .vx headers, commits as Vincent Ilagan,
# and pushes. Render.com redeploys https://lstore-n913.onrender.com/
# automatically about a minute later.
param([string]$Message = "Update LStore catalog and apps")
# Do NOT use -Stop: git writes harmless warnings (e.g. LF/CRLF) to stderr,
# which -Stop would treat as fatal. We check $LASTEXITCODE instead.
$ErrorActionPreference = "Continue"
Set-Location $PSScriptRoot
# Keep git quiet about end-of-line normalization noise.
git config core.autocrlf false 2>$null
git config core.safecrlf false 2>$null

Write-Host "==> Rebuilding catalog from apps\*.vx ..." -ForegroundColor Cyan
$pyExe = if (Get-Command py -ErrorAction SilentlyContinue) { "py" } else { "python" }
& $pyExe build_catalog.py
if ($LASTEXITCODE -ne 0) { Write-Host "catalog build failed" -ForegroundColor Red; exit 1 }

Write-Host "==> Committing as Vincent Ilagan ..." -ForegroundColor Cyan
git add -A
git -c user.name="Vincent Ilagan" -c user.email="vincentilagan@users.noreply.github.com" commit -m $Message
if ($LASTEXITCODE -ne 0) { Write-Host "(nothing new to commit - pushing anyway)" -ForegroundColor Yellow }

Write-Host "==> Pushing to GitHub ..." -ForegroundColor Cyan
git push origin main

Write-Host ""
Write-Host "Done. Render redeploys https://lstore-n913.onrender.com/ in about a minute." -ForegroundColor Green
