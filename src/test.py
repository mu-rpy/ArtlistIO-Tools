@echo off
setlocal

if exist ".setup_done" goto :run_script

:setup
if exist "LICENSE" (
    type "LICENSE"
    echo.
) else (
    echo [ERROR] LICENSE file not found.
    exit /b 1
)

set /p choice="Do you accept the license terms? (y/n): "
if /i "%choice%" neq "y" (
    echo [INFO] Exiting script.
    exit /b 0
)

python --version 2>nul | findstr /C:"3.14.2" >nul
if %errorlevel% neq 0 (
    echo [INFO] Python 3.14.2 not found. Downloading installer...
    curl -o python_installer.exe https://www.python.org/ftp/python/3.14.2/python-3.14.2-amd64.exe
    echo [INFO] Running installer...
    start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
    del python_installer.exe
)

echo [INFO] Installing pipenv...
pip install --quiet pipenv

if exist "Pipfile" (
    echo [INFO] Installing dependencies...
    pipenv install
) else (
    echo [ERROR] Pipfile not found.
)

echo. > .setup_done
echo [SUCCESS] Setup complete.

:run_script
echo [INFO] Starting application...
pipenv run python main.py
pause