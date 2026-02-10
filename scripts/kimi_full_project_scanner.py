import os
import sys
import argparse
from typing import List, Optional
try:
    from openai import OpenAI
except ImportError:
    print("[KIMI_SCANNER] ERROR: 'openai' library not found. Install it with 'pip install openai'.")
    sys.exit(1)

def load_env():
    env_file = os.path.join(os.path.dirname(__file__), "..", ".env")
    if os.path.exists(env_file):
        with open(env_file, "r") as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    os.environ[key] = value

class KimiProjectScanner:
    def __init__(self, api_key: Optional[str] = None):
        load_env()
        self.api_key = api_key or os.getenv("KIMI_API_KEY")
        if not self.api_key:
            raise ValueError("KIMI_API_KEY environment variable is not set.")
        
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.moonshot.cn/v1",
        )
        self.model = "moonshot-v1-128k" # High context model

    def scan_project(self, base_path: str, extensions: List[str] = [".md", ".py", ".txt"]):
        """Escanea el proyecto y recopila contenido de archivos relevantes."""
        print(f"[KIMI_SCANNER] Escaneando: {base_path}")
        context = []
        char_count = 0
        char_limit = 400000 # ~100k tokens hard limit for safety
        
        for root, dirs, files in os.walk(base_path):
            # Ignorar carpetas pesadas, irrelevantes o de sistema
            skip_dirs = [".git", "__pycache__", "node_modules", "evaluation", "logs", "brain", "tmp", ".gemini", ".vscode"]
            if any(x in root.split(os.sep) for x in skip_dirs):
                continue
                
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    if os.path.getsize(os.path.join(root, file)) > 100000: # Ignorar archivos > 100KB
                        continue
                    
                    try:
                        relative_path = os.path.relpath(os.path.join(root, file), base_path)
                        with open(os.path.join(root, file), "r", encoding="utf-8", errors="replace") as f:
                            content = f.read()
                            entry = f"--- FILE: {relative_path} ---\n{content}\n"
                            if char_count + len(entry) > char_limit:
                                print(f"[KIMI_SCANNER] Límite de contexto alcanzado ({char_limit}). Truncando escaneo.")
                                return "\n".join(context)
                            
                            context.append(entry)
                            char_count += len(entry)
                    except Exception as e:
                        print(f"[KIMI_SCANNER] Error leyendo {file}: {e}")
        
        return "\n".join(context)

    def analyze(self, project_context: str, query: str):
        """Envía todo el contexto a Kimi para su análisis masivo."""
        print("\n" + "="*50)
        print(" [MODELO: KIMI AI (MOONSHOT) - CONTEXTO ACTIVO] 🌙")
        print("="*50 + "\n")
        print(f"[KIMI_SCANNER] Enviando contexto a Kimi ({len(project_context)} caracteres)...")
        
        messages = [
            {"role": "system", "content": "Eres Antigravity (Kimi Mode), un Auditor Senior. Tienes acceso al contexto COMPLETO del proyecto. Responde de forma estratégica y técnica."},
            {"role": "user", "content": f"CONTEXTO DEL PROYECTO:\n{project_context}\n\nSOLICITUD: {query}"}
        ]
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error en la comunicación con Kimi: {e}"

def main():
    parser = argparse.ArgumentParser(description="Kimi Full Project Scanner (128k Context)")
    parser.add_argument("query", help="Qué quieres preguntar sobre el proyecto completo")
    parser.add_argument("-d", "--dir", default=".", help="Directorio raíz del proyecto")
    args = parser.parse_args()

    try:
        scanner = KimiProjectScanner()
        context = scanner.scan_project(args.dir)
        result = scanner.analyze(context, args.query)
        print("\n--- RESULTADO DEL ANÁLISIS DE KIMI ---\n")
        print(result)
    except Exception as e:
        print(f"[KIMI_SCANNER] ERROR: {e}")

if __name__ == "__main__":
    main()
