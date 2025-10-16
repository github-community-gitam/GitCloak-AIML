@echo off
title Invisibility Cloak Project

echo ================================
echo   Invisibility Cloak Project
echo ================================
echo.

:menu
echo Select an option:
echo 1. Run Setup (Check dependencies)
echo 2. Test Camera
echo 3. Basic Invisibility Cloak
echo 4. Advanced Invisibility Cloak
echo 5. Exit
echo.

set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto setup
if "%choice%"=="2" goto test_camera
if "%choice%"=="3" goto basic_cloak
if "%choice%"=="4" goto advanced_cloak
if "%choice%"=="5" goto exit
goto invalid

:setup
echo.
echo Running setup...
python setup.py
pause
goto menu

:test_camera
echo.
echo Testing camera...
python advanced_invisibility_cloak.py --test
pause
goto menu

:basic_cloak
echo.
echo Starting basic invisibility cloak...
python invisibility_cloak.py
pause
goto menu

:advanced_cloak
echo.
echo Starting advanced invisibility cloak...
python advanced_invisibility_cloak.py
pause
goto menu

:invalid
echo.
echo Invalid choice! Please enter 1-5.
echo.
goto menu

:exit
echo.
echo Goodbye!
pause
exit