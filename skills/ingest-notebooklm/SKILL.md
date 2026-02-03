---
name: ingest_notebooklm
description: Automate the extraction of knowledge from Google NotebookLM using the unofficial Python API wrapper (`notebooklm-py`).
triggers:
  - "leer mi cuaderno"
  - "usar notebooklm"
  - "conectar notebook"
---

# Ingestión de Conocimiento NotebookLM (API Wrapper)

## Objetivo
Acceder programáticamente a NotebookLM para extraer resúmenes, fuentes y chats de un cuaderno específico.

## Requisito Crítico: Cookies
Dado que no existe API pública, este método requiere que el usuario extraiga manualmente sus cookies de `notebooklm.google.com` UNA VEZ y las guarde.

1.  **Instalar extensión**: "Cookie-Editor" (o usar F12 DevTools).
2.  **Exportar**: Copiar las cookies en formato Netscape o JSON.
3.  **Guardar**: Crear archivo `notebooklm_cookies.txt` en la raíz del proyecto.

## Implementación Técnica

### 1. Librería
Usaremos `notebooklm-py` (o equivalente funcional) para manejar la comunicación RPC.

### 2. Script de Puente (`bridge.py`)
El agente debe generar y ejecutar este script cuando se le solicite:

```python
import os
from notebooklm import NotebookLMClient

def fetch_notebook_data(notebook_id):
    # Cargar cookies
    cookies_path = "notebooklm_cookies.txt"
    if not os.path.exists(cookies_path):
        print("ERROR: No se encontró 'notebooklm_cookies.txt'. Por favor exporta tus cookies.")
        return

    # Inicializar cliente
    client = NotebookLMClient(headers_or_cookies=cookies_path)
    
    # Obtener datos
    print(f"Conectando a cuaderno {notebook_id}...")
    notebook = client.get_notebook(notebook_id)
    
    # Salida
    print(f"--- TÍTULO: {notebook.title} ---")
    print(f"--- RESUMEN ---")
    print(notebook.summary)
    print(f"--- FUENTES ---")
    for source in notebook.sources:
        print(f"- {source.title}")

if __name__ == "__main__":
    # ID del cuaderno (extraído de la URL por el usuario o agente)
    NB_ID = os.getenv("NOTEBOOK_ID")
    fetch_notebook_data(NB_ID)
```

## Instrucciones de Uso para el Agente
Si el usuario pide conectar:
1.  Pide al usuario: "Por favor, pega la URL de tu cuaderno y asegúrate de tener el archivo `notebooklm_cookies.txt`".
2.  Extrae el `notebookId` de la URL.
3.  Ejecuta el script `bridge.py` pasando el ID.
4.  Lee la salida y úsala como contexto.
