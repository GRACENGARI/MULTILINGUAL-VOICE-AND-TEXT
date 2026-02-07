@echo off
REM Script to push African Language Tutor to GitHub (Windows)

echo ========================================
echo African Language AI Tutor - GitHub Push
echo ========================================

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed!
    echo Please install Git from: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo.
echo Step 1: Initializing Git repository...
if not exist .git (
    git init
    echo Git repository initialized!
) else (
    echo Git repository already exists.
)

echo.
echo Step 2: Adding files to Git...
git add .
echo Files added!

echo.
echo Step 3: Creating initial commit...
git commit -m "Initial commit: African Language AI Tutor with RAG architecture"
echo Commit created!

echo.
echo Step 4: Setting up GitHub remote...
echo.
echo Please enter your GitHub repository URL
echo Example: https://github.com/yourusername/african-language-tutor.git
set /p REPO_URL="Repository URL: "

if "%REPO_URL%"=="" (
    echo ERROR: No repository URL provided!
    pause
    exit /b 1
)

REM Check if remote already exists
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    git remote add origin %REPO_URL%
    echo Remote added!
) else (
    git remote set-url origin %REPO_URL%
    echo Remote updated!
)

echo.
echo Step 5: Pushing to GitHub...
git branch -M main
git push -u origin main

if errorlevel 1 (
    echo.
    echo ERROR: Push failed!
    echo.
    echo Possible solutions:
    echo 1. Make sure you created the repository on GitHub
    echo 2. Check your GitHub credentials
    echo 3. Try: git push -u origin main --force
    pause
    exit /b 1
)

echo.
echo ========================================
echo SUCCESS! Project pushed to GitHub!
echo ========================================
echo.
echo Your repository: %REPO_URL%
echo.
echo Next steps:
echo 1. Visit your GitHub repository
echo 2. Add a description and topics
echo 3. Enable GitHub Pages (optional)
echo 4. Share with the community!
echo.
pause