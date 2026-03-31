@echo off
echo 🚀 Starting Chrome in Debug Mode...

start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" ^
--remote-debugging-port=9222 ^
--user-data-dir="C:\chrome-profile"

echo.
echo 👉 Chrome opened.
echo 👉 Please login to ADDA manually.
echo 👉 Keep this Chrome open!
pause