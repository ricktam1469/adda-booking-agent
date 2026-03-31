@echo off
title Adda Booking Bot Installer

echo ======================================
echo 🚀 Installing Adda Booking Bot
echo ======================================

:: Step 1: Install uv
echo.
echo 🔧 Installing uv...
powershell -Command "irm https://astral.sh/uv/install.ps1 | iex"

:: Refresh PATH (important)
set PATH=%PATH%;%USERPROFILE%\.cargo\bin

echo.
echo 🔧 Setting up project...
uv sync

echo.
echo 🔧 Installing Playwright browsers...
uv run playwright install

echo.
echo ======================================
echo ✅ Installation Complete!
echo ======================================

echo.
echo 👉 Next Steps:
echo 1. Run open_chrome.bat and login
echo 2. Then run run.bat

pause