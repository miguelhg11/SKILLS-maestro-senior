echo ===================================================
cd /d "%~dp0"
echo ===================================================
echo      MAESTRO SKILL SYNC REPOSITORY MANAGER
echo ===================================================
echo.
echo [1/3] Downloading updates from Cloud (GitHub)...
git pull origin main
if %errorlevel% neq 0 (
    echo [WARNING] Git pull failed. Maybe no changes or network issue.
) else (
    echo [SUCCESS] Skills updated from cloud.
)

echo.
echo [2/3] Verifying dependencies (NotebookLM Bridge)...
pip install requests --quiet
if %errorlevel% neq 0 (
    echo [WARNING] Failed to install dependencies. Check Python/PIP.
) else (
    echo [SUCCESS] Dependencies verified.
)

echo.
echo [3/3] Uploading local changes to Cloud...
git add .
git commit -m "Auto-sync skills update [%date% %time%] - NotebookLM Standardized"
git push origin main
if %errorlevel% neq 0 (
    echo [WARNING] Git push failed. Check remote connection.
) else (
    echo [SUCCESS] Local skills uploaded to cloud.
)

echo.
echo ===================================================
echo      SYNC COMPLETE - ORCHESTRA TUNED
echo ===================================================
pause
