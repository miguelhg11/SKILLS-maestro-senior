@echo off
setlocal

:: Define Chrome Paths
set "CHROME_X64=C:\Program Files\Google\Chrome\Application\chrome.exe"
set "CHROME_X86=C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
set "USER_DATA=%USERPROFILE%\notebooklm_gateway_profile"

:: Detect Chrome
if exist "%CHROME_X64%" (
    set "CHROME_EXE=%CHROME_X64%"
) else if exist "%CHROME_X86%" (
    set "CHROME_EXE=%CHROME_X86%"
) else (
    echo Error: Google Chrome not found in standard locations.
    pause
    exit /b 1
)

echo [MAESTRO GATEWAY] Launching Chrome in Remote Debugging Mode...
echo [INFO] Profile Directory: %USER_DATA%
echo [INFO] Debug Port: 9222
echo.
echo INTRUCCIONES:
echo 1. Se abrira Chrome.
echo 2. Inicia sesion en NotebookLM si no lo estas.
echo 3. Manten esta ventana abierta mientras uses la AI.
echo.

"%CHROME_EXE%" --remote-debugging-port=9222 --user-data-dir="%USER_DATA%" --no-first-run --no-default-browser-check "https://notebooklm.google.com/"

echo.
echo [WARN] Chrome was closed. Connection lost.
pause
