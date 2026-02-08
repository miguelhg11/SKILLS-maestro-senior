---
description: Protocolo de cierre seguro de sesión Maestro Orchestrator
---

// turbo-all
# Cierro Sesión

Este workflow asegura que nada se pierda y el entorno quede limpio y sincronizado.

1. **Retorno Maestro**: Ejecuta el protocolo "**volver a Antigravity**" para restaurar el motor de orquestación central.
2. **Estado de Avance**: Crea o actualiza `POR_DONDE_VOY.md` resumiendo hitos, tareas pendientes y estado actual del proyecto.
// turbo
3. **Sincronización GitHub**: 
    - Realiza un commit con los avances de la sesión (v6.1).
    - Sube los cambios al repositorio remoto mediante `git push`.
4. **Walkthrough y Limpieza**: Genera el `walkthrough.md` final y elimina archivos temporales.
5. **Hibernación**: Notifica el cierre exitoso y se despide en modo orquestador.
