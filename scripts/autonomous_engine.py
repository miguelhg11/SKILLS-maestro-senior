import os
import sys
import subprocess
import json
try:
    from scripts.structured_logger import StructuredLogger
except ImportError:
    from structured_logger import StructuredLogger

class AutonomousEngine:
    """
    Motor de Autonomía Total v6.0 (Experimental)
    Implementa el loop: Plan -> Execute -> Verify -> Repair
    """
    def __init__(self):
        self.logger = StructuredLogger()
        self.context_bridge = "scripts/opencode_bridge.py"
        self.log_tag = "[AUTONOMOUS ENGINE v6.0]"

    def plan(self, objective):
        """Usa GPT-5.2 Codex para desglosar el objetivo en pasos ejecutables."""
        print(f"{self.log_tag} Planificando objetivo: {objective}")
        self.logger.log_compliance_check("v6.0_PLANNING", "IN_PROGRESS", f"Objective: {objective}")
        
        prompt = (
            f"Objective: {objective} \n"
            "Environment: Windows PowerShell / Maestro skills v5.0 \n"
            "Return ONLY a raw JSON object (no markdown, no explanations) with this structure: "
            "{'steps': [{'command': 'shell_command', 'description': 'step_description'}]}"
        )
        
        plan_raw = self._get_opencode_output(prompt)
        try:
            # Limpiar posible basura de la terminal si existe
            json_start = plan_raw.find('{')
            json_end = plan_raw.rfind('}') + 1
            plan_data = json.loads(plan_raw[json_start:json_end])
            self.logger.log_event("PLAN_GENERATED", plan_data)
            return plan_data.get('steps', [])
        except Exception as e:
            self.logger.log_event("PLAN_PARSE_ERROR", {"error": str(e), "raw": plan_raw})
            return []

    def verify(self, step):
        """Verifica el éxito de un paso delegando la comprobación a GPT."""
        command = step.get('command')
        desc = step.get('description')
        print(f"{self.log_tag} Verificando Step: {desc}")
        
        prompt = (
            f"Command executed: {command} \n"
            f"Description: {desc} \n"
            "Analyze if this step was likely successful based on its intent. "
            "Return ONLY 'SUCCESS' or 'FAILURE'."
        )
        
        verification = self._get_opencode_output(prompt).strip()
        is_success = "SUCCESS" in verification.upper()
        
        self.logger.log_compliance_check(f"VERIFY_{desc[:20]}", "SUCCESS" if is_success else "FAILED")
        return is_success

    def repair(self, failed_step, error_msg):
        """Solicita a GPT un paso de remediación ante un fallo detectado."""
        print(f"{self.log_tag} Iniciando REPAIR para: {failed_step.get('description')}")
        self.logger.log_event("REPAIR_START", {"failed_step": failed_step, "error": error_msg})
        
        prompt = (
            f"The following step failed: {failed_step.get('description')} \n"
            f"Command: {failed_step.get('command')} \n"
            f"Error message: {error_msg} \n"
            "Provide a new set of commands to fix the issue and achieve the original goal. "
            "Return ONLY a raw JSON: {'steps': [{'command': 'shell_command', 'description': 'repair_description'}]}"
        )
        
        repair_plan = self._get_opencode_output(prompt)
        try:
            json_start = repair_plan.find('{')
            json_end = repair_plan.rfind('}') + 1
            repair_steps = json.loads(repair_plan[json_start:json_end]).get('steps', [])
            
            for r_step in repair_steps:
                if self.execute_step(r_step):
                    if self.verify(r_step):
                        self.logger.log_event("REPAIR_SUCCESS", r_step)
                        return True
            return False
        except Exception as e:
            self.logger.log_event("REPAIR_PARSE_ERROR", {"error": str(e)})
            return False

    def run_autonomous_loop(self, objective):
        """Ejecuta el ciclo completo P-E-V-R."""
        steps = self.plan(objective)
        if not steps:
            print(f"{self.log_tag} Fallo al generar el plan.")
            return False

        for step in steps:
            success = self.execute_step(step)
            if not success:
                print(f"{self.log_tag} Fallo detectado. Iniciando remediación...")
                if not self.repair(step, "Execution error in shell"):
                    print(f"{self.log_tag} La remediación automática falló.")
                    self.logger.log_event("LOOP_ABORTED", {"step": step})
                    return False
            
            if not self.verify(step):
                print(f"{self.log_tag} Validación semántica fallida. Reintentando...")
                if not self.repair(step, "Semantic verification failed"):
                    print(f"{self.log_tag} Falló la verificación de remediación.")
                    return False
        
        self.logger.log_event("LOOP_COMPLETED", {"objective": objective})
        return True

    def execute_step(self, step):
        command = step.get('command')
        desc = step.get('description')
        print(f"{self.log_tag} Ejecutando Step: {desc}")
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                self.logger.log_event("STEP_SUCCESS", {"command": command})
                return True
            else:
                self.logger.log_event("STEP_FAILED", {"command": command, "error": result.stderr})
                return False
        except Exception as e:
            self.logger.log_event("EXECUTION_EXCEPTION", {"error": str(e)})
            return False

    def _get_opencode_output(self, prompt):
        """Lanza la consulta y extrae el texto de salida."""
        try:
            cmd = ["opencode", "run", "-m", "openai/gpt-5.2-codex", prompt]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return result.stdout
        except Exception as e:
            return str(e)

if __name__ == "__main__":
    engine = AutonomousEngine()
    print("Motor Autónomo v6.0 inicializado.")
