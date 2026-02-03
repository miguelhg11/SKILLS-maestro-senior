---
name: ingest_notebooklm
description: Automate the extraction of knowledge from Google NotebookLM using browser automation (Playwright/Puppeteer) as a bridge since no public API exists.
triggers:
  - "leer mi cuaderno"
  - "usar notebooklm"
  - "conectar notebook"
---

# Ingestión de Conocimiento NotebookLM (Browser Bridge)

## Objetivo
Acceder y extraer información de un "Cuaderno" (Notebook) de Google NotebookLM para usarlo como contexto en tareas de generación de video o código.

## Limitación Técnica
NotebookLM **NO tiene API pública**.
**Solución**: Usamos un Agente de Navegación (Browser Agent) simulando un usuario humano.

## Requisitos
1.  **Habilidad Base**: El agente debe tener acceso a `building-browser-agents` (Playwright/Puppeteer).
2.  **Autenticación**:
    *   *Opción A (Interactivo)*: El agente abre el navegador en modo "con cabeza" (headed), el usuario se loguea manualmente, y el agente guarda el estado (`auth.json`).
    *   *Opción B (Cookies)*: El usuario exporta sus cookies de Google a `notebooklm_cookies.json`.

## Flujo de Ejecución (Script Conceptual)

### 1. Inicialización
*   El agente verifica si tiene credenciales válidas.
*   Lanza navegador: `https://notebooklm.google.com/`.

### 2. Navegación
*   Identifica la lista de cuadernos.
*   Selecciona el cuaderno especificado por el usuario (ej: "Lanzamiento Producto").
*   Navega a la sección de "Fuentes" o "Chat".

### 3. Extracción (Scraping)
*   **Modo Resumen**: Extrae el "Resumen del Cuaderno" (Audio Overview transcript o texto generado).
*   **Modo Consulta**: Envía un prompt al chat de NotebookLM: *"Resume los puntos clave para un video de 30s"*.
*   Captura la respuesta del DOM.

### 4. Salida
*   Guarda la información extraída en `temp/notebook_context.txt`.
*   Pasa este contexto a la siguiente skill (ej: `remotion-video`).

## Instrucción para el Agente (runtime)
> *"Si el usuario pide conectar NotebookLM, utiliza la herramienta `browser_action` para navegar a la URL. Si encuentras un muro de login, pausa y solicita al usuario que se autentique en la ventana abierta."*
