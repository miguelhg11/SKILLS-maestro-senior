---
description: Protocolo de inicio de sesión Maestro Orchestrator
---

// turbo-all
# Comenzamos Sesión

Este workflow asegura que el entorno esté afinado y sincronizado antes de empezar a trabajar.

1. **Sincronización Cloud**: Ejecuta `.\maestro_sync.bat` para bajar los últimos cambios y subir los locales.
// turbo
2. **Audit de Skills**: Escanea la carpeta `skills/` para identificar capacidades relevantes para el proyecto actual.
3. **Verificación de Seguridad**: Asegura que archivos sensibles (.env, cookies) estén en `.gitignore`.
4. **Resumen de Estado**: Proporciona un breve resumen al usuario de lo que se ha sincronizado y la preparación del "Maestro".
5. **Captura de Objetivo**: Solicita al usuario el objetivo principal de la sesión de hoy.
6. **Alineación Maestro**: Re-afirma y activa todas las directrices de `PROMPT_MAESTRO.md` para la nueva sesión.
