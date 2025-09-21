@echo off
echo.
echo  ████████████████████████████████████████████████████████████████████
echo  █                                                                  █
echo  █              🚀 PUSH TO GITHUB - SMART DOC CHECKER               █
echo  █                                                                  █
echo  ████████████████████████████████████████████████████████████████████
echo.

echo This script will help you push your code to GitHub
echo.

:GET_USERNAME
set /p github_username="Enter your GitHub username: "
if "%github_username%"=="" (
    echo Please enter a valid username!
    goto GET_USERNAME
)

echo.
echo Using GitHub username: %github_username%
echo Repository URL will be: https://github.com/%github_username%/smart-doc-checker
echo.

set /p confirm="Is this correct? (y/n): "
if /i not "%confirm%"=="y" goto GET_USERNAME

echo.
echo 📡 Adding GitHub remote...
git remote remove origin 2>nul
git remote add origin https://github.com/%github_username%/smart-doc-checker.git

echo.
echo 📤 Pushing to GitHub...
git branch -M main
git push -u origin main

if %errorlevel% neq 0 (
    echo.
    echo ❌ Push failed! Make sure:
    echo 1. You created the repository on GitHub
    echo 2. Your GitHub credentials are set up
    echo 3. The repository name is exactly: smart-doc-checker
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ SUCCESS! Your code is now on GitHub!
echo.
echo 🌐 Repository URL: https://github.com/%github_username%/smart-doc-checker
echo.
echo 🚀 Next steps:
echo 1. Go to https://share.streamlit.io
echo 2. Sign in with GitHub
echo 3. Deploy your app using repository: %github_username%/smart-doc-checker
echo 4. Set main file as: app.py
echo.
echo Your app will be live forever at a Streamlit URL!
echo.
pause
