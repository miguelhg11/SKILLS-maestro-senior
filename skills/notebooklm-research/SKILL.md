---
name: consult_notebooklm
description: Consulta investigaciones, documentos y notas almacenadas en NotebookLM para obtener respuestas sin alucinaciones.
triggers:
  - "busca en mis notas"
  - "consulta notebooklm"
  - "investiga en el cuaderno"
  - "usa mi investigación"
---

# NotebookLM Research Skill

## Objetivo
Utilizar el servidor MCP de NotebookLM para responder preguntas complejas basándose estrictamente en las fuentes proporcionadas por el usuario, evitando alucinaciones.

## Instrucciones de Uso (Protocolo Gateway - Estándar 2026)

**IMPORTANTE**: El método de cookies manuales ha sido deprecado. Se debe usar el **Protocolo Gateway** (CDP).

### 1. Iniciar el Gateway (Paso Humano Único)
El navegador debe ser una instancia controlada por el usuario para evitar bloqueos de Google.
1. Ejecutar `open_notebook_gateway.bat` desde la raíz del proyecto.
2. Iniciar sesión en NotebookLM en la ventana de Chrome que se abre.
3. **Mantener esa ventana abierta** (puede estar minimizada).

### 2. Uso con el Servidor MCP
El script `scripts/notebooklm_mcp_server.py` se conectará automáticamente al Gateway abierto ("Conexión Quirúrgica").

**Comandos Disponibles:**
- **Listar Cuadernos**:
  ```bash
  python scripts/notebooklm_mcp_server.py --list
  ```
- **Leer Cuaderno**:
  ```bash
  python scripts/notebooklm_mcp_server.py --fetch <NOTEBOOK_ID>
  ```
  *(El ID es la cadena alfanumérica al final de la URL del cuaderno)*.

### 3. Solución de Problemas
- **User data directory is already in use**: Cierra todas las ventanas de Chrome de ese perfil o reinicia el Gateway.
- **Connection Refused**: Asegúrate de que `open_notebook_gateway.bat` sigue corriendo.

## Flujo de Trabajo
1. Validar que el Gateway está activo (`--test-cdp`).
2. Listar/Seleccionar cuaderno.
3. Extraer conocimiento (`--fetch`).
4. Integrar en el proyecto.

