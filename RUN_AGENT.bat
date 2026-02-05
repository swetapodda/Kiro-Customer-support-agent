@echo off
echo ============================================================
echo Credit Card Customer Support Agent
echo ============================================================
echo.

REM Check if .env file exists
if not exist ".env" (
    echo ERROR: .env file not found!
    echo.
    echo Please create .env file:
    echo   1. Copy .env.example to .env
    echo   2. Edit .env and add your API key
    echo   3. Get key from: https://makersuite.google.com/app/apikey
    echo.
    pause
    exit /b 1
)

python src/unified_agent.py

echo.
echo ============================================================
pause
