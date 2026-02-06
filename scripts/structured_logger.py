import json
import os
import time
from datetime import datetime

class StructuredLogger:
    """
    Logger Senior para el Maestro Orchestrator.
    Registra decisiones, skills usadas y cumplimiento de reglas en formato JSON.
    """
    def __init__(self, log_dir="logs/orchestration"):
        self.log_dir = log_dir
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        self.session_id = f"session_{int(time.time())}"
        self.log_file = os.path.join(self.log_dir, f"{self.session_id}.jsonl")

    def log_event(self, event_type, details):
        """Registra un evento estructurado."""
        event = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "session_id": self.session_id,
            "event_type": event_type,
            "details": details
        }
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(event) + "\n")

    def log_skill_usage(self, skill_name, purpose, success=True):
        self.log_event("SKILL_USAGE", {
            "skill": skill_name,
            "purpose": purpose,
            "success": success
        })

    def log_compliance_check(self, rule_id, status, observation=""):
        self.log_event("COMPLIANCE_CHECK", {
            "rule_id": rule_id,
            "status": status,
            "observation": observation
        })

    def log_delegation(self, target_model, task_summary):
        self.log_event("DELEGATION", {
            "target_model": target_model,
            "task": task_summary
        })

if __name__ == "__main__":
    # Test rápido de integridad
    logger = StructuredLogger()
    logger.log_event("BOOTSTRAP", {"version": "5.0", "status": "active"})
    print(f"Logger activo. Sesion: {logger.session_id}")
