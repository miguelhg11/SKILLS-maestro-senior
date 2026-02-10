# PROTOCOLO DE MODOS DE OPERACIÓN (MAESTRO V6.2)

Este documento define la ley marcial sobre qué "cerebro" ejecuta qué tarea.

## SISTEMA DE MODOS (PERSISTENTE Global)

El modo activo se guarda en `.env` bajo `MAESTRO_MODE`. Afecta a **todo** el proyecto y a cualquier sub-agente invocado.

### 1. 🤖 MODO AUTO (Por Defecto)
*   **Comando**: `"Ponte en modo auto"`, `"Reset mode"`, `"Modo híbrido"`.
*   **Valor ENV**: `MAESTRO_MODE=AUTO`
*   **Lógica**:
    *   **GPT-4o (Browser Bridge)**: Es el **JEFE**. Planifica y ejecuta Backend, Lógica y Sistemas.
    *   **Kimi AI**: Es el **ESPECIALISTA**. Ejecuta Frontend (HTML/CSS), Diseño y Análisis de Contexto Masivo.
    *   **Grok 3 (SALVAGUARDA)**: **NO se usa automáticamente**. Si la tarea lo requiere, el sistema presentará una `[SUGERENCIA]`. El usuario debe confirmar cambiando a Modo Grok.

---

## FLUJO DE ÓRDENES Y JERARQUÍA

1.  **ENTRADA**: El usuario define un objetivo (vía voz o texto).
2.  **PLANIFICACIÓN**: GPT evalúa la tarea y genera pasos técnicos en formato JSON.
3.  **ORQUESTACIÓN (En Modo AUTO)**:
    *   `Step de Lógica/Datos` -> Se envía a **GPT**.
    *   `Step de Frontend/CSS/UI` -> Se envía a **Kimi**.
    *   `Step de Investigación Real-Time/Deep` -> Se emite **Sugerencia de Grok** (Safe-Mode).
4.  **CONTROL DE USUARIO**:
    *   Podrás decir `"Modo Grok"` en cualquier momento para que **Grok** tome el control total (Modo Experimental/Alto Razonamiento).
    *   Cada respuesta indicará: `[MODELO ACTIVO]`.

### 2. ⚡ MODO GPT ONLY
*   **Comando**: `"Solo usa GPT"`, `"Modo GPT"`, `"Force GPT"`.
*   **Valor ENV**: `MAESTRO_MODE=GPT_ONLY`
*   **Lógica**:
    *   **GPT-4o**: Ejecuta **TODO**. Frontend, Backend, Diseño.
    *   **Kimi**: Desactivado/Prohibido.
    *   *Uso*: Cuando necesitas razonamiento complejo en todas las capas o prefieres el estilo de código de OpenAI.

### 3. 🚀 MODO GROK ONLY (xAI)
*   **Comando**: `"Ponte en modo Grok"`, `"Solo usa Grok"`, `"Investiga con Grok"`.
*   **Valor ENV**: `MAESTRO_MODE=GROK_ONLY`
*   **Lógica**:
    *   **Grok 3 (xAI)**: Ejecuta **TODO**.
    *   **Puntos Fuertes**: Información en tiempo real (X), razonamiento profundo, contexto de 1M tokens.
    *   *Uso*: Investigación de tendencias, noticias de última hora o depuración de problemas de vanguardia.

## SOPORTE DE MODELOS EXTERNOS (Futuro)
*   La arquitectura permite añadir `CLAUDE_ONLY` o `DEEPSEEK_ONLY` siguiendo el mismo patrón en `autonomous_engine.py`.

## COMANDOS DE MANDO RECONOCIDOS (Voz/Texto)
El sistema intercepta automáticamente frases como:
*   "Usa Kimi"
*   "Cambia a GPT"
*   "Ponte en modo Grok"
*   "Vuelve a modo automático"
*   "Resetea el motor"

---
**ESTADO ACTUAL**: Verifica el encabezado de cada respuesta del Agente para saber quién te habla.
