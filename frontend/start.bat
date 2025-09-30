@echo off
echo Starting Document Extractor Frontend...
echo.

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

REM Check if we're in the frontend directory
if not exist "package.json" (
    echo ERROR: package.json not found
    echo Make sure you're running this from the frontend directory
    pause
    exit /b 1
)

REM Install dependencies if node_modules doesn't exist
if not exist "node_modules" (
    echo Installing dependencies...
    npm install
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Check if .env file exists
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env
)

echo.
echo Starting React development server...
echo Frontend will be available at: http://localhost:3000
echo Backend should be running at: http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo.

npm start

pause