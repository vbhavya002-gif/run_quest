@echo off
setlocal
cd /d "%~dp0"
set "PY="
where py >nul 2>nul && set "PY=py"
if not defined PY where python >nul 2>nul && set "PY=python"
if not defined PY goto nopython
%PY% -c "import pygame" >nul 2>nul || %PY% -m pip install -r requirements.txt
%PY% main.py
if errorlevel 1 pause
exit /b
:nopython
echo Python was not found.
echo Install it from https://www.python.org/downloads/
echo and tick "Add python.exe to PATH" during setup, then run this file again.
pause
