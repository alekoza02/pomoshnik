@echo off

REM Fetch the latest changes
git fetch

REM Ensure the branch tracks the remote branch
git branch --set-upstream-to=origin/main

REM Get the local and remote commit hashes
for /f %%i in ('git rev-parse HEAD') do set LOCAL=%%i
for /f %%i in ('git rev-parse @{u}') do set REMOTE=%%i

REM Check if the local version is up to date
if "%LOCAL%"=="%REMOTE%" (
    echo Repository is up to date.
) else (
    echo New version detected, updating...
    git reset --hard HEAD
    git pull origin main
)

REM After update (or if already up to date), launch main.py
echo Launching main.py...
py.exe main.py

echo To remove the exit, edit the main.bat
pause