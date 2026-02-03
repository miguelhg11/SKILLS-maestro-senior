@echo off
echo ===================================================
echo      MAESTRO SKILL SYNC REPOSITORY MANAGER
echo ===================================================
echo.
echo [1/2] Downloading updates from Cloud (GitHub)...
git pull origin main
if %errorlevel% neq 0 (
    echo [WARNING] Git pull failed. Maybe no changes or network issue.
) else (
    echo [SUCCESS] Skills updated from cloud.
)

echo.
echo [2/2] Uploading local changes to Cloud...
git add .
git commit -m "Auto-sync skills update [%date% %time%]"
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
