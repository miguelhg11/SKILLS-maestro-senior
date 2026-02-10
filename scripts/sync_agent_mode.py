import os
import sys

def sync_mode():
    """
    Reads the MAESTRO_MODE from .env and prints it in a format
    that can be consumed by other scripts or the OpenCode context.
    """
    env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
    mode = "AUTO"
    
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("MAESTRO_MODE="):
                    mode = line.strip().split("=")[1]
                    break
    
    # Output specifically formatted for context injection
    print(f"MAESTRO_SYSTEM_MODE={mode}")
    print(f"ACTIVE_MODEL_MANDATE={mode}")
    
    if mode == "KIMI_ONLY":
        print("INSTRUCTION: ALL SUB-AGENTS MUST USE KIMI AI (MOONSHOT). DO NOT USE GPT.")
    elif mode == "GPT_ONLY":
        print("INSTRUCTION: ALL SUB-AGENTS MUST USE GPT-5.2 CODEX. DO NOT USE KIMI.")
    
if __name__ == "__main__":
    sync_mode()
