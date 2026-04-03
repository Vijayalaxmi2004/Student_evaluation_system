@echo off
REM Quick deployment script for Windows PowerShell
REM This script will help you push code to GitHub in a few steps

echo.
echo ====================================
echo  GitHub Deployment Script
echo ====================================
echo.

REM Step 1: Check if git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Git is not installed or not in PATH
    echo Download from: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo [1/5] Git is installed ✓
echo.

REM Step 2: Check current directory
if not exist "app.py" (
    echo ERROR: app.py not found in current directory
    echo Please run this script from the Student_evaluation_system folder
    pause
    exit /b 1
)

echo [2/5] Found app.py ✓
echo.

REM Step 3: Initialize git (if not already initialized)
if not exist ".git" (
    echo [3/5] Initializing git repository...
    git init
    echo Git repository initialized ✓
) else (
    echo [3/5] Git repository already exists ✓
)

echo.

REM Step 4: Add files and commit
echo [4/5] Staging files and creating initial commit...
git add .
git commit -m "Initial commit: Student Evaluation System with Attendance and Mid Marks Analysis"
echo Files staged and committed ✓
echo.

REM Step 5: Instructions for user
echo [5/5] Ready to push to GitHub!
echo.
echo ====================================
echo NEXT STEPS:
echo ====================================
echo.
echo 1. Create a new repository on GitHub:
echo    - Go to https://github.com/new
echo    - Name: Student_Evaluation_System
echo    - Make it PUBLIC
echo    - Click "Create repository"
echo.
echo 2. Copy the HTTPS URL from GitHub (looks like):
echo    https://github.com/YOUR_USERNAME/Student_Evaluation_System.git
echo.
echo 3. Run these commands in PowerShell:
echo.
echo    git remote add origin https://github.com/YOUR_USERNAME/Student_Evaluation_System.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 4. Then deploy on Streamlit Cloud:
echo    - Go to https://share.streamlit.io/
echo    - Click "New app"
echo    - Select your repository
echo    - Set main file to "app.py"
echo    - Click Deploy!
echo.
echo Your app will be live at:
echo https://share.streamlit.io/YOUR_USERNAME/Student_Evaluation_System
echo.
echo ====================================
echo.
pause
