@echo off
:: open_gpt_gateway.bat
:: Launches Chrome with Remote Debugging Port 9222 for GPT/OpenCode Bridge
:: This allows the Python script to "piggyback" on your logged-in session.

echo [GPT GATEWAY] Launching Chrome Secure Gateway...
echo.
echo    1. Chrome will open.
echo    2. Log in to ChatGPT (https://chatgpt.com) if not already logged in.
echo    3. Keep the window OPEN. The bridge needs it to send prompts.
echo.

:: Path to Chrome (Standard Windows locations)
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    set CHROME_PATH="C:\Program Files\Google\Chrome\Application\chrome.exe"
) else (
    set CHROME_PATH="C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
)

:: User Data Dir to persist login sessions (Note: Using separate profile to avoid conflicts)
set USER_DATA_DIR="%USERPROFILE%\.gpt_bridge_profile"

start "" %CHROME_PATH% --remote-debugging-port=9222 --user-data-dir=%USER_DATA_DIR% "https://chatgpt.com"

echo [GPT GATEWAY] Chrome launched on port 9222.
echo [GPT GATEWAY] You can now use 'opencode run' commands.
pause
