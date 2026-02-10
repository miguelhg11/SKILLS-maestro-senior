import os
import sys
from autonomous_engine import AutonomousEngine

def test_mode(mode_name):
    print(f"\n--- TESTING MODE: {mode_name} ---")
    os.environ["MAESTRO_MODE"] = mode_name
    engine = AutonomousEngine()
    
    # We want to check the internal logic without actually calling the expensive/slow LLMs if possible,
    # or at least verify what it TRIES to do.
    # However, since we can't mock easily without extra libs, we will rely on the print statements
    # we added in autonomous_engine.py which print the mode and model.
    
    # We will try to plan a simple objective.
    # It might fail if no LLM key is present or if opencode is not connected, but we catch that.
    try:
        engine.plan("Say hello")
    except Exception as e:
        print(f"Caught expected exception (network/auth/parsing): {e}")

if __name__ == "__main__":
    # Test 1: GPT_ONLY
    test_mode("GPT_ONLY")
    
    # Test 2: KIMI_ONLY
    test_mode("KIMI_ONLY")
    
    # Test 3: AUTO
    test_mode("AUTO")
