@echo off
echo Starting SentriX - Multi-Agent Supply Chain Risk Intelligence Platform
echo.

echo Installing dependencies...
call npm run install-all

echo.
echo Starting SentriX...
echo Backend will run on http://localhost:8000
echo Frontend will run on http://localhost:3000
echo.

call npm run dev

pause
