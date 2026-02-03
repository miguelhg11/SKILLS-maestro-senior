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

## Instrucciones de Uso (Herramientas MCP)

1. **Selección de Cuaderno:**
   - Si no se especifica cuaderno, usa `list_notebooks` para mostrar opciones.
   - Si se especifica, usa `select_notebook` indicando el ID o nombre.

2. **Consulta:**
   - Usa `ask_question` para enviar la consulta al cuaderno seleccionado.
   - Pide siempre la cita (`citation`) para validar.

3. **Manejo de Autenticación:**
   - Si las herramientas de NotebookLM no aparecen o fallan, solicita al usuario ejecutar el comando `mcp login-notebooklm` en la terminal.

## Flujo de Trabajo
1. Detectar intención de búsqueda.
2. Listar/Seleccionar cuaderno.
3. Consultar datos.
4. Integrar respuesta en el proyecto actual (Código, Video, etc.).
