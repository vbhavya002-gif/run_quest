@echo off
setlocal
cd /d "%~dp0"
set "PY="
where py >nul 2>nul && set "PY=py"
if not defined PY where python >nul 2>nul && set "PY=python"
if not defined PY goto nopython
echo Installing pygame and PyInstaller...
%PY% -m pip install -r requirements.txt pyinstaller
echo Building RuneQuest.exe ...
%PY% -m PyInstaller --noconfirm --onefile --windowed --name RuneQuest --icon icon.ico main.py
echo.
echo Done! Your game is here: dist\RuneQuest.exe
echo You can copy that single file to any Windows PC and double-click it.
pause
exit /b
:nopython
echo Python was not found. Install it from https://www.python.org/downloads/
echo and tick "Add python.exe to PATH", then run this file again.
pause
