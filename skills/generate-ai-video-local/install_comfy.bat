@echo off
echo ===================================================
echo   COMFYUI LOCAL INSTALLER (NVIDIA GPU REQUIRED)
echo ===================================================

echo Checking for Git...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Git is not installed. Please install Git first.
    exit /b 1
)

echo Checking for Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed. Please install Python 3.10+.
    exit /b 1
)

:: Set installation directory
set "INSTALL_DIR=%~dp0..\..\..\ComfyUI_Local"
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

cd /d "%INSTALL_DIR%"

echo [1/3] Cloning ComfyUI Repository...
if not exist "ComfyUI" (
    git clone https://github.com/comfyanonymous/ComfyUI.git
) else (
    echo ComfyUI already cloned. Skipping.
)

cd ComfyUI

echo [2/3] Installing Dependencies (Torch + Requirements)...
:: Assuming standard Python. Better to use venv in real life, but keeping simple for script.
pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu121
pip install -r requirements.txt

echo [3/3] Setting up Stable Video Diffusion (SVD)...
set "CHECKPOINTS_DIR=models\checkpoints"
if not exist "%CHECKPOINTS_DIR%" mkdir "%CHECKPOINTS_DIR%"

echo.
echo [INFO] Ready to download SVD Models (svd_xt.safetensors).
echo [INFO] This file is large (9GB+).
echo [ACTION] Press any key to download, or verify if you have it manually.
pause

curl -L -o "%CHECKPOINTS_DIR%\svd_xt.safetensors" "https://huggingface.co/stabilityai/stable-video-diffusion-img2vid-xt/resolve/main/svd_xt.safetensors?download=true"

echo.
echo ===================================================
echo   INSTALLATION COMPLETE.
echo   To run: cd "%INSTALL_DIR%\ComfyUI" && python main.py
echo ===================================================
pause
