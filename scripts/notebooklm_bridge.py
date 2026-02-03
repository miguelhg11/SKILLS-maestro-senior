import os
import sys
import json
import requests
from typing import Optional

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
                # Intentar cargar como JSON (extensión Cookie-Editor)
                try:
                    cookies_json = json.loads(content)
                    for cookie in cookies_json:
                        self.session.cookies.set(cookie['name'], cookie['value'], domain=cookie.get('domain', '.google.com'))
                except json.JSONDecodeError:
                    # Intentar cargar como Netscape/Text (formato alternativo)
                    print("Cargando cookies en formato texto/Netscape...")
                    # Implementación simplificada para pares clave=valor por línea
                    for line in content.splitlines():
                        if not line.startswith('#') and '\t' in line:
                            parts = line.split('\t')
                            if len(parts) >= 7:
                                self.session.cookies.set(parts[5], parts[6], domain=parts[0])
            return True
        except Exception as e:
            print(f"Error al cargar cookies: {e}")
            return False

    def fetch_notebook(self, notebook_id: str):
        print(f"Intentando acceder al cuaderno: {notebook_id}...")
        url = f"{self.base_url}/notebook/{notebook_id}"
        
        # Primero intentamos una petición normal para verificar sesión
        response = self.session.get(url)
        
        if response.status_code == 200 and "Sign in" not in response.text:
            print("¡Conexión exitosa! Sesión válida.")
            # Aquí iría la lógica de extracción de datos via RPC
            # Nota: Esto es un puente estructural para verificar conexión
            return True
        else:
            print(f"Error: No se pudo acceder. Código: {response.status_code}")
            if "Sign in" in response.text:
                print("La sesión parece haber expirado o las cookies son inválidas.")
            return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python notebooklm_bridge.py <notebook_id>")
        sys.exit(1)
        
    nb_id = sys.argv[1]
    bridge = NotebookLMBridge()
    if bridge.load_cookies():
        if bridge.fetch_notebook(nb_id):
            print("Sistema listo para ingesta de datos.")
        else:
            sys.exit(1)
    else:
        sys.exit(1)
