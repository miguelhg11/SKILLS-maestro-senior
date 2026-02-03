---
name: generate_ai_video_local
description: Generate AI video (Image-to-Video) locally using ComfyUI + Stable Video Diffusion. Requires NVIDIA GPU (8GB+).
triggers:
  - "animar esta imagen"
  - "video con ia local"
  - "stable video diffusion"
---

# Generación de Video IA Local (ComfyUI)

## Objetivo
Animar imágenes estáticas (Image-to-Video) utilizando modelos generativos (SVD) ejecutados en el hardware local del usuario (GPU NVIDIA), sin coste de API.

## Requisitos de Hardware
- **GPU**: NVIDIA RTX 3060 (12GB) o superior recomendada. (Mínimo 8GB).
- **RAM**: 16GB+.
- **Espacio**: 20GB libres.

## Prerrequisitos de Software
1.  **ComfyUI Instalado**: El motor debe estar presente en `../../ComfyUI_Local`.
    -   *Si no existe*: Ejecuta el script `install_comfy.bat` incluido en esta carpeta.
2.  **Modelos**: El checkpoint `svd_xt.safetensors` debe estar descargado.

## Flujo de Trabajo (Workflow)

### 1. Inicialización
*   Verifica si el servidor de ComfyUI está corriendo (puerto 8188).
*   Si no, inícialo:
    ```cmd
    cd [RUTA_COMFYUI]
    python main.py
    ```

### 2. Generación (API)
*   **Input**: Imagen base (ruta local).
*   **Parámetros**:
    *   `motion_bucket_id`: 127 (movimiento estándar).
    *   `augmentation_level`: 0.02 (fidelidad).
*   **Acción**: Envía el JSON de workflow a `http://127.0.0.1:8188/prompt`.
    *   *Nota*: El workflow JSON para SVD debe estar precargado o construido dinámicamente.

### 3. Resultado
*   ComfyUI guardará el video en su carpeta `output/`.
*   Mueve el archivo resultante a la carpeta del proyecto del usuario.

## Manejo de Errores
- **OOM (Out of Memory)**: Si la GPU falla, sugiere reducir la resolución o "tiling".
- **Falta de Modelo**: Si falla la carga, solicita al usuario ejecutar el instalador.
