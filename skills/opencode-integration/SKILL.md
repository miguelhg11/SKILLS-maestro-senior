---
name: opencode-integration
description: Integra y orquesta el uso de modelos de lenguaje desde el CLI de OpenCode (opencode.ai) dentro del flujo de trabajo de Antigravity. Permite utilizar modelos como GPT-5.2 Codex y GLM-4.7 manteniendo el contexto local del proyecto.
---

# OpenCode Integration (Skill)

## Propósito
Permitir que el Agente Antigravity delegue tareas de programación, refactorización y análisis a los modelos configurados en la cuenta de OpenCode del usuario, actuando como un puente de contexto.

## Protocolo de Autenticación
- **Verificación**: Antes de operar, ejecutar `opencode auth`.
- **Login**: Si no hay sesión activa, solicitar al usuario ejecutar `opencode auth login`.
- **Seguridad**: Las API Keys se gestionan internamente por el CLI de OpenCode; nunca exponerlas en logs.

## Gestión de Modelos
- **Listado**: `opencode models` para ver opciones disponibles.
- **Selección**: Usar el flag `-m <model_id>` en los comandos de chat o apply.
- **Modelos Recomendados**: 
  - `openai/gpt-5.2-codex` para generación de código compleja.
  - `opencode/glm-4.7-free` para consultas rápidas y análisis.

## Inyección de Contexto (Antigravity -> OpenCode)
Para que el modelo de OpenCode trabaje con el contexto del proyecto Antigravity:
1. **Paso de Archivos**: Al usar `opencode chat`, incluir los archivos relevantes del proyecto.
2. **Contexto de Sesión**: Antigravity debe resumir el estado actual del proyecto antes de realizar la petición a OpenCode.

## Comandos de Operación
- **Consulta/Ejecución**: `opencode run "mensaje"`
- **Intervención Directa**: `opencode [directorio]` para abrir la TUI en un contexto específico.
- **Modelos**: `opencode run --model <provider/model> "mensaje"`
- **Configuración**: `opencode config` para parámetros globales.

## Protocolo de Conmutación (Hot-Swap & Persistente)
- **Activación GPT**: `"ir a GPT"` -> Antigravity entra en **ESTADO DELEGADO PERSISTENTE**. Todas las tareas se envían a GPT y los reportes llevan el tag `[MODELO ACTIVO: GPT CODEX (PLUS)]`.
- **Retorno Antigravity**: `"ir a Antigravity"` -> Se desactiva la persistencia y se restaura el encabezado a `[MODELO ACTIVO: ANTIGRAVITY (GEMINI)]`.

## Inyección de Contexto (Handover Senior)
Para una transición perfecta:
1. **Snapshot**: Ejecutar `python scripts/opencode_bridge.py`.
2. **Handoff**: `opencode run "CONTEXT: [Cargar snapshot] TAREA: [Descripción detallada]"`
3. **Audit de Regreso**: Al volver a Gemini, realizar un `git status` y `grep` para identificar el impacto de los cambios de OpenCode.

## Reglas de Oro (Senior)
1. **Soberanía de Diseño**: Antigravity mantiene la visión arquitectónica; OpenCode ejecuta la implementación técnica.
2. **Duda Metódica**: Si OpenCode altera archivos críticos del núcleo sin previo aviso, Antigravity debe alertar y proponer rollback.
3. **Sincronización Continua**: Cada cambio de OpenCode debe ser "asimilado" por Antigravity antes de continuar con la orquestación.
