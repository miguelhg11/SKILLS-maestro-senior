# Flujo de Trabajo Maestro (Maestro Workflow)

Este documento define el Procedimiento Operativo Estándar (SOP) para trabajar con el sistema **SKILLS-maestro-senior** en múltiples equipos.

## 1. Configuración Inicial (Solo 1 vez por Ordenador)

Si llegas a un ordenador nuevo (ej: Equipo B):

1.  **Instalar Git**: Asegúrate de tener Git instalado.
2.  **Clonar el Cerebro**:
    Abre una terminal en la carpeta donde quieras guardar las skills y ejecuta:
    ```cmd
    git clone https://github.com/miguelhg11/SKILLS-maestro-senior.git
    ```
    *Ahora tienes una copia local de la inteligencia colectiva.*

## 2. Rutina Diaria (Inicio de Sesión)

Cada vez que empieces a trabajar en un proyecto (sea cual sea, Ej: "Cuentos Infantiles", "APP Web", etc.):

1.  **Abre tu Proyecto**: Abre tu editor (Cursor/VS Code) en la carpeta de TU proyecto.
2.  **Pega el Prompt Maestro**: Copia y pega el "Prompt de Activación" en el chat del Agente.
3.  **El Agente toma el mando**:
    *   **Paso A (Sync)**: El Agente ejecutará `maestro_sync.bat` (buscando la ruta de skills que le digas). Esto bajará las últimas novedades de la nube.
    *   **Paso B (Audit)**: El Agente verificará que tiene todas las herramientas necesarias.
    *   **Paso C (Work)**: Empezará a trabajar en tu proyecto usando esa inteligencia.

## 3. Durante el Trabajo (Crecimiento)

Si el Agente descubre que necesita una habilidad nueva (ej: "Manejo de PDFs"):
1.  El Agente creará el archivo `skills/handling-pdfs/SKILL.md`.
2.  El Agente registrará la skill en `marketplace.json`.
3.  *El sistema local ya es más inteligente.*

## 4. Cierre de Sesión (Guardado)

Al terminar el día o el hito:
1.  El Agente (o tú manualmente) ejecuta `maestro_sync.bat`.
2.  El script sube (`push`) las nuevas skills a GitHub.
3.  *La nube ya es más inteligente.*

## 5. Al día siguiente (En el otro equipo)

1.  Empiezas la **Rutina Diaria (Punto 2)**.
2.  Al ejecutarse el `maestro_sync.bat` automático, **descarga la skill "Manejo de PDFs"** que creaste ayer en el otro equipo.
3.  El Agente en el Equipo B ya sabe manejar PDFs.

---
**Resumen**:
*   **Prompt Maestro**: La llave de encendido.
*   **Maestro Sync**: El motor de sincronización.
*   **GitHub**: El cerebro central.
