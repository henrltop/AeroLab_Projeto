@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if not errorlevel 1 (
  py -3 "%~dp0server_local.py"
  if errorlevel 1 pause
  exit /b
)
where python >nul 2>nul
if not errorlevel 1 (
  python "%~dp0server_local.py"
  if errorlevel 1 pause
  exit /b
)
echo Python nao encontrado. Abra dist\Painel_Ventoinha.html no Chrome ou Edge.
start "" "%~dp0dist\Painel_Ventoinha.html"
pause
