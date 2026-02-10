
import sys
import os

# Ensure we can import from local scripts
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from autonomous_engine import AutonomousEngine
except ImportError:
    # Adjust path if running from root
    sys.path.append(os.path.join(os.getcwd(), 'scripts'))
    from autonomous_engine import AutonomousEngine

class MockAutonomousEngine(AutonomousEngine):
    def _get_llm_output(self, prompt):
        print("\n--- GENERATED PROMPT PREVIEW ---")
        print(prompt)
        print("--------------------------------\n")
        return '{"steps": []}'

def test_prompt_content():
    engine = MockAutonomousEngine()
    print("Testing prompt generation for frontend task...")
    engine.plan("Create a login page with CSS")

if __name__ == "__main__":
    test_prompt_content()
