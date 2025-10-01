@echo off
title Upload Invisibility Cloak to GitHub

echo ======================================
echo   Upload Invisibility Cloak to GitHub
echo ======================================
echo.

echo This script will help you upload your project to GitHub.
echo Make sure you have:
echo   1. A GitHub account
echo   2. Git installed on your computer
echo   3. Created a new empty repository on GitHub
echo.

pause

echo.
echo Step 1: Initialize Git repository
git init

echo.
echo Step 2: Add all files to Git
git add .

echo.
echo Step 3: Create initial commit
git commit -m "Initial commit: Invisibility Cloak Project"

echo.
echo Step 4: Set default branch to main
git branch -M main

echo.
echo Now you need to connect to your GitHub repository.
echo.
echo Please:
echo 1. Go to https://github.com
echo 2. Click "New" to create a new repository
echo 3. Name it something like "invisibility-cloak-project"
echo 4. Do NOT initialize with README (since we already have files)
echo 5. Copy the repository URL (it looks like: https://github.com/yourusername/repositoryname.git)
echo.

set /p repo_url="Enter your GitHub repository URL: "

echo.
echo Step 5: Connect to GitHub repository
git remote add origin %repo_url%

echo.
echo Step 6: Push to GitHub
git push -u origin main

echo.
echo ===============================================
echo   Upload Complete!
echo ===============================================
echo.
echo Your project should now be available at:
echo %repo_url%
echo.
echo You can now:
echo - Share your project with others
echo - Track changes over time
echo - Collaborate with other developers
echo.

pause