---
name: generate_remotion_video
description: Create programmatic video using Remotion AI based on research content from NotebookLM.
triggers:
  - "crear un video sobre"
  - "generar video explicativo"
  - "renderizar video con remotion"
---

# Generación de Video con Remotion y NotebookLM

## Objetivo
Transformar texto y datos de investigación almacenados en NotebookLM en un archivo de video MP4 renderizado utilizando la biblioteca React Remotion.

## Prerrequisitos
- El servidor MCP de NotebookLM debe estar activo y autenticado.
- El proyecto Remotion debe estar inicializado en la carpeta `./video-engine` (si no existe, el agente debe crearlo con `npx create-video@latest`).

## Pasos de Ejecución

1.  **Obtener Contexto (Fase de Investigación):**
    - Consulta NotebookLM: "Dame un guion estructurado para un video de [DURACIÓN] segundos sobre [TEMA], incluyendo títulos, subtítulos y códigos de color preferidos."
    - Validad que la respuesta incluya:
        - `title`: Título principal.
        - `sections`: Lista de secciones con texto y duración estimada.
        - `colors`: Paleta de colores (hex).

2.  **Generar Código (Fase de Codificación):**
    - Localiza el archivo `./video-engine/src/Composition.tsx`.
    - REESCRIBE el componente `MyComposition` (o equivalente) para reflejar el guion.
    - **Patrón de Diseño**:
        - Usa componentes `<Sequence>` para cada sección del guion.
        - Usa `useCurrentFrame` y `interpolate` para animaciones suaves de entrada/salida.
        - Usa `<AbsoluteFill>` para fondos con los colores extraídos.
        - Usa `<staticFile>` si necesitas cargar imágenes locales, o genera componentes geométricos/texto.

3.  **Renderizar (Fase de Producción):**
    - Abre una terminal en `./video-engine`.
    - Ejecuta: `npx remotion render MyComp out/video.mp4` (ajusta el nombre de la composición según `Root.tsx`).
    - **Verificación**: Comprueba con `Get-Item` si `out/video.mp4` existe y tiene un tamaño > 0.
    - Reporta la ubicación final absoluta al usuario: "Video renderizado en: [RUTA]".

## Manejo de Errores (Self-Healing)
- **Error de Compilación**: Si `npx remotion render` falla, LEE el log de error.
    - *Causa Común*: Error de sintaxis en `Composition.tsx` o falta de dependencias.
    - *Acción*: Corrige el archivo y reintenta.
- **Error de Dependencias**: Si faltan paquetes, ejecuta `npm install`.

## Ejemplo de Código (Composition.tsx)

```tsx
import { AbsoluteFill, Sequence, useCurrentFrame, interpolate } from 'remotion';

export const MyComposition = () => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 30], [0, 1]);

  return (
    <AbsoluteFill style={{ backgroundColor: 'white' }}>
      <Sequence durationInFrames={150}>
        <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center' }}>
          <h1 style={{ opacity }}>Título del Video</h1>
        </AbsoluteFill>
      </Sequence>
      {/* Añadir más secuencias aquí */}
    </AbsoluteFill>
  );
};
```
