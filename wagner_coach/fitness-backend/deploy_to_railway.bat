@echo off
echo ========================================
echo Railway Deployment Script
echo ========================================
echo.

cd /d %~dp0

echo Checking if git is initialized...
if not exist ".git" (
    echo Initializing git repository...
    git init
    git branch -M main
)

echo.
echo Adding all changes...
git add .

echo.
echo Creating commit...
git commit -m "Fix: Complete requirements.txt and Railway config for deployment"

echo.
echo ========================================
echo NEXT STEPS:
echo ========================================
echo.
echo 1. Go to Railway Dashboard: https://railway.app
echo 2. Click your "Fitness-App" service
echo 3. Click "Settings" tab
echo 4. Scroll to "Service Source"
echo 5. Connect to GitHub or use Railway CLI
echo.
echo OR use Railway CLI:
echo   railway login
echo   railway link
echo   railway up
echo.
echo Then set environment variables in Railway Dashboard!
echo ========================================
pause