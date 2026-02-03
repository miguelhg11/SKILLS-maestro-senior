import os
import sys
import json
import requests
import re
from typing import Optional, List, Dict

class NotebookLMBridge:
    def __init__(self, cookies_path: str = "notebooklm_cookies.txt"):
        self.cookies_path = cookies_path
        self.session = requests.Session()
        self.base_url = "https://notebooklm.google.com"

    def load_cookies(self) -> bool:
        if not os.path.exists(self.cookies_path):
            print(f"Error: No se encontró el archivo '{self.cookies_path}'")
            return False
        
        try:
            with open(self.cookies_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                try:
                    cookies_json = json.loads(content)
                    for cookie in cookies_json:
                        self.session.cookies.set(cookie['name'], cookie['value'], domain=cookie.get('domain', '.google.com'))
                except json.JSONDecodeError:
                    for line in content.splitlines():
                        if not line.startswith('#') and '\t' in line:
                            parts = line.split('\t')
                            if len(parts) >= 7:
                                self.session.cookies.set(parts[5], parts[6], domain=parts[0])
            return True
        except Exception as e:
            print(f"Error al cargar cookies: {e}")
            return False

    def list_notebooks(self) -> List[Dict[str, str]]:
        """Intenta listar los cuadernos disponibles en la cuenta."""
        print("Obteniendo lista de cuadernos...")
        response = self.session.get(self.base_url)
        if response.status_code != 200:
            print(f"Error al acceder a la home: {response.status_code}")
            return []
            
        # NotebookLM carga datos vía JS/RPC. Buscamos patrones de IDs en el HTML como fallback
        # o buscamos bloques de datos iniciales.
        notebooks = []
        # Pattern match for common notebook ID structure in JSON blobs
        matches = re.findall(r'\"([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})\"', response.text)
        
        # Este es un método heurístico. En una implementación pro, buscaríamos el endpoint RPC.
        # Por ahora, si no hay IDs, pedimos el ID directo.
        if not matches:
            print("No se pudieron detectar cuadernos automáticamente. Es posible que el contenido sea dinámico.")
        
        unique_ids = list(set(matches))
        for uid in unique_ids:
            notebooks.append({"id": uid, "title": "Cargando..."})
            
        return notebooks

    def get_sources(self, notebook_id: str) -> bool:
        """Intenta extraer las fuentes del cuaderno analizando el HTML."""
        url = f"{self.base_url}/notebook/{notebook_id}"
        print(f"Obteniendo fuentes del cuaderno: {notebook_id}...")
        
        response = self.session.get(url)
        if response.status_code != 200:
            print(f"Error al acceder al cuaderno: {response.status_code}")
            return False
            
        with open("notebook_dump.html", "w", encoding="utf-8") as f:
            f.write(response.text)
        print("Dump de contenido guardado en 'notebook_dump.html'")

        # Extraer bloques de datos
        data_blocks = re.findall(r'AF_initDataCallback\((.*?)\);', response.text, re.DOTALL)
        sources_found = []
        
        for block in data_blocks:
            try:
                # Limpiar el bloque para intentar cargarlo como JSON o lista de Python
                # A menudo tiene formato: {key: 'ds:1', hash: '...', data: [...]}
                # Buscamos la parte 'data:'
                data_match = re.search(r'data:(.*)', block, re.DOTALL)
                if data_match:
                    data_str = data_match.group(1).strip()
                    # Eliminar coma final si existe
                    if data_str.endswith(','): data_str = data_str[:-1]
                    
                    # Intentar cargar como JSON (a veces requiere correcciones de comillas)
                    try:
                        data_json = json.loads(data_str)
                        # Buscar recursivamente strings que parezcan contenido de búsqueda
                        self._find_content(data_json, sources_found)
                    except:
                        continue
            except:
                continue

        if sources_found:
            print(f"Se encontraron {len(sources_found)} fragmentos de contenido relevante.")
            with open("extracted_research.txt", "w", encoding="utf-8") as f:
                for s in sources_found:
                    f.write(f"--- FRAGMENTO ---\n{s}\n\n")
            return True
        else:
            print("No se pudo extraer contenido estructurado. El cuaderno podría estar vacío o el formato cambió.")
            return False

    def _find_content(self, obj, found_list):
        if isinstance(obj, str):
            if len(obj) > 100 and any(keyword in obj.lower() for keyword in ["tendencia", "diseño", "web", "maestro", "mejora"]):
                found_list.append(obj)
        elif isinstance(obj, list):
            for item in obj:
                self._find_content(item, found_list)
        elif isinstance(obj, dict):
            for val in obj.values():
                self._find_content(val, found_list)

    def fetch_notebook(self, notebook_id: str):
        print(f"Intentando acceder al cuaderno: {notebook_id}...")
        url = f"{self.base_url}/notebook/{notebook_id}"
        response = self.session.get(url)
        
    def ask_question(self, notebook_id: str, query: str):
        print(f"Enviando consulta al cuaderno: {query}")
        # Endpoint RPC para consultas
        url = f"{self.base_url}/_/NotebookLMSkillService/AskQuestion"
        
        # Payload simplificado basado en inspección previa de tráfico RPC
        # Nota: Los parámetros exactos pueden variar, buscamos consistencia.
        payload = [
            notebook_id,
            query,
            None, # parent_message_id
            None, # exploration_id
            True  # include_citations
        ]
        
        headers = {
            "Content-Type": "application/json+protobuf", # NotebookLM suele usar Protobuf sobre JSON
            "X-Goog-AuthUser": "0",
            "Referer": f"{self.base_url}/notebook/{notebook_id}"
        }
        
        response = self.session.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            try:
                # El formato de respuesta de Google RPC suele ser un array con el primer elemento como prefijo
                data = response.json()
                print("Respuesta recibida.")
                # Extraemos el texto de la respuesta (heurística basada en estructura común)
                # En una implementación real, esto requeriría parsear el esquema exacto.
                # Por ahora, devolvemos el JSON para análisis del agente.
                return data
            except:
                print(f"Error al procesar respuesta: {response.text[:200]}")
                return None
        else:
            print(f"Error en consulta (Código: {response.status_code})")
            return None

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Antigravity NotebookLM Bridge")
    parser.add_argument("id", nargs="?", help="ID del cuaderno a consultar")
    parser.add_argument("--list", action="store_true", help="Listar cuadernos disponibles")
    parser.add_argument("--query", help="Pregunta para el cuaderno")
    parser.add_argument("--sources", action="store_true", help="Intentar listar fuentes")
    
    args = parser.parse_args()
    bridge = NotebookLMBridge()
    
    if not bridge.load_cookies():
        sys.exit(1)
        
    if args.list:
        notebooks = bridge.list_notebooks()
        if notebooks:
            print("Cuadernos detectados (Heurística):")
            for nb in notebooks:
                print(f"- {nb['id']}")
        else:
            print("No se encontraron cuadernos.")
    elif args.id:
        if args.query:
            result = bridge.ask_question(args.id, args.query)
            if result:
                print(json.dumps(result, indent=2))
            else:
                sys.exit(1)
        elif args.sources:
            result = bridge.get_sources(args.id)
            if isinstance(result, str):
                # Guardar en archivo temporal si es muy largo
                with open("notebook_content.html", "w", encoding="utf-8") as f:
                    f.write(result)
                print("Contenido guardado en 'notebook_content.html'.")
            elif result:
                print(json.dumps(result, indent=2))
        else:
            if bridge.fetch_notebook(args.id):
                print("Sistema listo.")
            else:
                sys.exit(1)
    else:
        parser.print_help()
