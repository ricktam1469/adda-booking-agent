@echo off

echo 🚀 Setting up environment...

REM Install dependencies
uv sync

REM Install Playwright browser
uv run playwright install

echo.
echo 🚀 Starting Booking Bot...

uv run python booking_bot.py

pause