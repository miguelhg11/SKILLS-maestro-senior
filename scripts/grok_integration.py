import os
import sys
import argparse
from openai import OpenAI
from dotenv import load_dotenv

# Cargar variables de entorno desde .archivos locales
load_dotenv()

# Configuración
XAI_API_KEY = os.getenv("XAI_API_KEY")
BASE_URL = "https://api.x.ai/v1"

def get_grok_response(prompt, model="grok-3"):
    """
    Envía un prompt a Grok (xAI) y retorna la respuesta.
    """
    if not XAI_API_KEY:
        return "Error: XAI_API_KEY no encontrada en .env. Por favor añádela."

    try:
        client = OpenAI(
            api_key=XAI_API_KEY,
            base_url=BASE_URL,
        )

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are Grok, an AI developed by xAI. Answer with your characteristic wit and directness if appropriate, but always be helpful."},
                {"role": "user", "content": prompt},
            ],
        )

        return response.choices[0].message.content
    except Exception as e:
        return f"Error connecting to Grok API: {str(e)}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Grok Integration Bridge")
    parser.add_argument("prompt", type=str, help="Prompt to send to Grok")
    parser.add_argument("--model", type=str, default="grok-3", help="Model to use (default: grok-3)")
    
    args = parser.parse_args()
    
    # Simple output for pipe integration
    print(get_grok_response(args.prompt, args.model))
