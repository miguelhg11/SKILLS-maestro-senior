import os
import sys
import argparse
import logging
from typing import Optional, List
try:
    from openai import OpenAI
except ImportError:
    print("Error: 'openai' package not found. Please run 'pip install openai'")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="[KIMI_INTEGRATION] %(levelname)s: %(message)s"
)
logger = logging.getLogger(__name__)

def load_env():
    env_file = os.path.join(os.path.dirname(__file__), "..", ".env")
    if os.path.exists(env_file):
        with open(env_file, "r") as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    os.environ[key] = value

class KimiClient:
    def __init__(self, api_key: Optional[str] = None):
        load_env()
        self.api_key = api_key or os.getenv("KIMI_API_KEY")
        if not self.api_key:
            raise ValueError("KIMI_API_KEY environment variable is not set.")
        
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.moonshot.cn/v1",
        )
        # Default model
        self.default_model = "moonshot-v1-8k" # Standard model, can be overridden

    def chat(self, message: str, model: Optional[str] = None, system_prompt: Optional[str] = None, context_files: Optional[List[str]] = None) -> str:
        model = model or self.default_model
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        else:
             messages.append({"role": "system", "content": "You are Kimi, a helpful AI assistant integrated into the Maestro system."})

        # Inject context from files if provided
        if context_files:
            file_context = ""
            for file_path in context_files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        file_context += f"\n--- FILE: {os.path.basename(file_path)} ---\n{content}\n"
                except Exception as e:
                    logger.warning(f"Failed to read context file {file_path}: {e}")
            
            if file_context:
                message = f"CONTEXT:\n{file_context}\n\nUSER REQUEST:\n{message}"

        messages.append({"role": "user", "content": message})

        try:
            logger.info(f"Sending request to Kimi API (Model: {model})")
            completion = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.3, # Low temperature for more deterministic code/analysis
            )
            response_content = completion.choices[0].message.content
            return response_content
        except Exception as e:
            logger.error(f"API Request failed: {e}")
            return f"Error communicating with Kimi API: {e}"

    def list_models(self):
        try:
            # Moonshot API might not support standard list models endpoint exactly like OpenAI, 
            # but we can try or just return known models.
            # For now, let's return a hardcoded list of known Moonshot models as per documentation 
            # to avoid API issues if the endpoint differs.
            return [
                "moonshot-v1-8k",
                "moonshot-v1-32k",
                "moonshot-v1-128k"
            ]
        except Exception as e:
            logger.error(f"Failed to list models: {e}")
            return []

def main():
    parser = argparse.ArgumentParser(description="Kimi AI Integration CLI")
    parser.add_argument("message", nargs="?", help="Message to send to Kimi")
    parser.add_argument("-m", "--model", help="Model to use (default: moonshot-v1-8k)")
    parser.add_argument("-f", "--file", action="append", help="Context files to include")
    parser.add_argument("--system", help="System prompt override")
    parser.add_argument("--test", action="store_true", help="Run a connection test")
    
    args = parser.parse_args()

    try:
        client = KimiClient()
    except ValueError as e:
        logger.error(str(e))
        sys.exit(1)

    if args.test:
        print("Testing Kimi AI connection...")
        response = client.chat("Hello! Are you online?", model="moonshot-v1-8k")
        print(f"Response: {response}")
        return

    if not args.message:
        parser.print_help()
        return

    response = client.chat(
        message=args.message,
        model=args.model,
        system_prompt=args.system,
        context_files=args.file
    )
    
    # Print response to stdout for capture
    print(response)

if __name__ == "__main__":
    main()
