---
name: kimi-integration
description: Integra y orquesta el uso del modelo Kimi AI (Moonshot) dentro del flujo de trabajo de Maestro. Especializado en manejo de contextos largos y razonamiento en chino/inglés/español.
---

# Kimi AI Integration (Skill)

## Propósito
Permitir que el Agente Maestro delegue tareas de análisis, resumen y generación de código a Kimi AI (Moonshot), aprovechando su gran ventana de contexto (hasta 128k tokens) y capacidad de razonamiento.

## Requisitos Previos
- Variable de entorno `KIMI_API_KEY` configurada.
- Paquete Python `openai` instalado.

## Comandos de Operación
La integración se realiza a través del script `scripts/kimi_integration.py`.

### Consultas Simples
Para consultas rápidas sin contexto de archivos:
`python scripts/kimi_integration.py "Tu pregunta aquí" -m moonshot-v1-8k`

### Análisis con Contexto de Archivos
Para analizar código o documentos específicos:
`python scripts/kimi_integration.py "Analiza este código y busca errores" -f path/to/file1.py -f path/to/file2.md`

### Modelos Disponibles
- `moonshot-v1-8k`: Consultas estándar, respuestas rápidas.
- `moonshot-v1-32k`: Análisis de documentos medianos.
- `moonshot-v1-128k`: Análisis de bases de código grandes o documentos extensos.

## Casos de Uso Recomendados
1. **Resumen de Documentación Extensa**: Usar modelo 128k para resumir múltiples archivos o documentación técnica larga.
2. **Análisis de Código Cruzado**: Evaluar dependencias entre varios archivos de scripts.
3. **Segunda Opinión**: Obtener una perspectiva alternativa a la de Gemini/GPT sobre una arquitectura o problema lógico.

## Protocolo de Errores
- Si el script devuelve error de autenticación, verificar `KIMI_API_KEY`.
- Si hay timeout, reintentar con un modelo de menor contexto o reducir la cantidad de archivos a los estrictamente necesarios.

## Protocolo de Persistencia (Senior)
Cuando el Maestro entra en modo `CONTINUIDAD ACTIVA` con Kimi:
1. **Delegación de Tareas**: Todas las consultas entrantes se procesan primero a través de `kimi_integration.py`.
2. **Visual Feedback**: Se debe incluir el encabezado `[SISTEMA: GENERADO POR KIMI AI - CONTINUIDAD ACTIVA]` en cada interacción.
3. **Escalado de Memoria**: En modo persistente, se debe priorizar el modelo `moonshot-v1-32k` para balancear velocidad y contexto, escalando a `128k` solo cuando el contexto supere los 30k tokens.
