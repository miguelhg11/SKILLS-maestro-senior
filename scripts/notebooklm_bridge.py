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

    def fetch_notebook(self, notebook_id: str):
        print(f"Intentando acceder al cuaderno: {notebook_id}...")
        url = f"{self.base_url}/notebook/{notebook_id}"
        response = self.session.get(url)
        
        if response.status_code == 200 and "Sign in" not in response.text:
            # Extraer título del notebook
            title_match = re.search(r'<title>(.*?)</title>', response.text)
            title = title_match.group(1) if title_match else "Sin título"
            print(f"¡Conexión exitosa! Título detectado: {title}")
            return True
        else:
            print(f"Error: No se pudo acceder (Código: {response.status_code})")
            return False

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Antigravity NotebookLM Bridge")
    parser.add_argument("id", nargs="?", help="ID del cuaderno a consultar")
    parser.add_argument("--list", action="store_true", help="Listar cuadernos disponibles")
    
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
        if bridge.fetch_notebook(args.id):
            print("Sistema listo.")
        else:
            sys.exit(1)
    else:
        parser.print_help()
