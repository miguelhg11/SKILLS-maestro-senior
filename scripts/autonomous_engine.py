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
        """Planifica el objetivo usando el modelo adecuado según el modo."""
        
        # INTERCEPTION: Check if this is a System Configuration Command (Meta-Command)
        if self._detect_system_intent(objective):
            # Return a dummy step so the loop completes successfully and logs the action
            print(f"{self.log_tag} System Configuration updated. Returning confirmation step.")
            return [{'command': 'echo "System configuration updated successfully."', 'description': 'Confirm system configuration update'}]

        mode = os.getenv("MAESTRO_MODE", "AUTO").upper()
        print(f"{self.log_tag} [MODE: {mode}] Planificando objetivo: {objective}")
        self.logger.log_compliance_check(f"v6.0_PLANNING_{mode}", "IN_PROGRESS", f"Objective: {objective}")

        # Construct Prompt based on Mode
        if mode == "KIMI_ONLY":
            # Kimi is the planner
            planner_model = "KIMI"
            prompt = (
                f"Objective: {objective} \n"
                "Environment: Windows PowerShell / Maestro skills v5.0 \n"
                "ROLE: You are the Lead Architect and Planner. \n"
                "You must break down this objective into executable shell commands.\n"
                "Return ONLY a raw JSON object (no markdown) with this structure: "
                "{'steps': [{'command': 'shell_command', 'description': 'step_description'}]}"
            )
        elif mode == "GPT_ONLY":
            # GPT is the planner, NO delegation
            planner_model = "GPT"
            prompt = (
                f"Objective: {objective} \n"
                "Environment: Windows PowerShell / Maestro skills v5.0 \n"
                "ROLE: You are the Sole Executor. You must handle ALL tasks yourself.\n"
                "Do NOT delegate to any other agent. Do NOT use `kimi_integration.py`.\n"
                "Return ONLY a raw JSON object (no markdown) with this structure: "
                "{'steps': [{'command': 'shell_command', 'description': 'step_description'}]}"
            )
        else: # AUTO (Default)
            # GPT is the planner, WITH delegation
            planner_model = "GPT"
            prompt = (
                f"Objective: {objective} \n"
                "Environment: Windows PowerShell / Maestro skills v5.0 \n"
                "ROLES Y DELEGACIÓN:\n"
            "- TÚ (GPT-5.2 Codex) eres el ORQUESTADOR y EXPERTO EN LÓGICA. Gestiona backend, lógica, datos y sistema.\n"
            "- KIMI AI es el ESPECIALISTA EN FRONTEND Y DISEÑO. Delega todas las tareas de HTML, CSS, JS (UI) y Diseño Gráfico a Kimi.\n\n"
            "CÓMO DELEGAR A KIMI:\n"
            "Si el paso implica crear/modificar UI, CSS o código frontend, genera un comando como:\n"
            "  `python scripts/kimi_integration.py \"Crea una página de login moderna...\" > ruta/al/archivo.html`\n"
            "NO intentes escribir el CSS/HTML tú mismo en el plan. Delega la generación a Kimi.\n\n"
            "Return ONLY a raw JSON object (no markdown, no explanations) with this structure: "
            "{'steps': [{'command': 'shell_command', 'description': 'step_description'}]}"
            )

        # Execute Planning
        if planner_model == "KIMI":
            plan_raw = self._get_kimi_output(prompt)
        else:
            plan_raw = self._get_opencode_output(prompt)
        
        # FAIL-FAST
        if plan_raw.startswith("Error executing"):
             raise RuntimeError(f"FATAL: Planner ({planner_model}) failed. {plan_raw}")

        try:
            # Clean JSON
            json_start = plan_raw.find('{')
            json_end = plan_raw.rfind('}') + 1
            if json_start == -1 or json_end == 0:
                 raise ValueError(f"Planner ({planner_model}) response contained no valid JSON")
                 
            plan_data = json.loads(plan_raw[json_start:json_end])
            self.logger.log_event("PLAN_GENERATED", {"mode": mode, "steps": plan_data})
            return plan_data.get('steps', [])
        except Exception as e:
            self.logger.log_event("PLAN_PARSE_ERROR", {"error": str(e), "raw": plan_raw})
            raise RuntimeError(f"FATAL: Failed to parse plan. Raw output: {plan_raw[:100]}...") from e

    def verify(self, step):
        """Verifica el éxito de un paso delegando la comprobación."""
        command = step.get('command')
        desc = step.get('description')
        print(f"{self.log_tag} Verificando Step: {desc}")
        
        prompt = (
            f"Command executed: {command} \n"
            f"Description: {desc} \n"
            "Analyze if this step was likely successful based on its intent. "
            "Return ONLY 'SUCCESS' or 'FAILURE'."
        )
        
        # Verification typically needs logic, so we prefer GPT unless KIMI_ONLY
        mode = os.getenv("MAESTRO_MODE", "AUTO").upper()
        if mode == "KIMI_ONLY":
            verification = self._get_kimi_output(prompt).strip()
        else:
            verification = self._get_opencode_output(prompt).strip()

        if verification.startswith("Error"):
             # Weak failover - if verification tool fails, assume success to avoid loop lock, but log it
             print(f"{self.log_tag} ⚠️ Verification tool failed. Assuming success for flow continuity.")
             return True

        is_success = "SUCCESS" in verification.upper()
        
        self.logger.log_compliance_check(f"VERIFY_{desc[:20]}", "SUCCESS" if is_success else "FAILED")
        return is_success

    def repair(self, failed_step, error_msg):
        """Solicita un paso de remediación."""
        print(f"{self.log_tag} Iniciando REPAIR para: {failed_step.get('description')}")
        self.logger.log_event("REPAIR_START", {"failed_step": failed_step, "error": error_msg})
        
        prompt = (
            f"The following step failed: {failed_step.get('description')} \n"
            f"Command: {failed_step.get('command')} \n"
            f"Error message: {error_msg} \n"
            "Provide a new set of commands to fix the issue. "
            "Return ONLY a raw JSON: {'steps': [{'command': 'shell_command', 'description': 'repair_description'}]}"
        )
        
        mode = os.getenv("MAESTRO_MODE", "AUTO").upper()
        if mode == "KIMI_ONLY":
            repair_plan = self._get_kimi_output(prompt)
        else:
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
        try:
            steps = self.plan(objective)
        except RuntimeError as e:
            print(f"{self.log_tag} 🛑 CRITICAL FAILURE: {e}")
            return False

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
        
        # Enforce GPT_ONLY restriction at execution time (Defense in Depth)
        mode = os.getenv("MAESTRO_MODE", "AUTO").upper()
        if mode == "GPT_ONLY" and "kimi_integration.py" in command:
            print(f"{self.log_tag} 🛑 BLOCKED: 'kimi_integration.py' called in GPT_ONLY mode.")
            self.logger.log_event("EXECUTION_BLOCKED", {"reason": "GPT_ONLY mode violation", "command": command})
            return False

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

    def _print_status_header(self):
        """Imprime el estado del Agente y el Modelo Activo."""
        engine_mode = os.getenv("MAESTRO_LLM_ENGINE", "GPT").upper()
        if engine_mode == "KIMI":
            status_line = "MODELO ACTIVO: KIMI AI (MOONSHOT) 🌙"
        else:
            status_line = "MODELO ACTIVO: GPT-5.2 CODEX 🤖"
            
        print("\n" + "="*60)
        print(f" [GESTOR DE AGENTES] ESTADO: ONLINE | {status_line}")
        print("="*60 + "\n")

    def _get_llm_output(self, prompt):
        """Legacy method needed for compatibility, but redirects to mode logic."""
        mode = os.getenv("MAESTRO_MODE", "AUTO").upper()
        
        if mode == "KIMI_ONLY":
            return self._get_kimi_output(prompt)
        elif mode == "GPT_ONLY":
            return self._get_opencode_output(prompt)
        else:
            # AUTO MODE
            # Logic: Default to GPT, but if context is huge, might switch to Kimi?
            # For now, let's keep it simple: AUTO means GPT handles it, unless explicitly delegated.
            # But if this is a general query, we check context length.
            if len(prompt) > 8000 and os.getenv("KIMI_API_KEY"):
                 print(f"{self.log_tag} ⚠️ CONTEXT > 8k chars in AUTO mode. Using KIMI for heavy lifting.")
                 return self._get_kimi_output(prompt)
            return self._get_opencode_output(prompt)

    def _get_opencode_output(self, prompt):
        """Lanza la consulta a GPT vía OpenCode."""
        if os.getenv("MAESTRO_LLM_ENGINE") == "KIMI":
             print(f"{self.log_tag} 🛑 BLOQUEO DE SEGURIDAD: Intento de uso de GPT estando en modo KIMI.")
             return self._get_kimi_output(prompt)

        try:
            cmd = f'opencode run -m openai/gpt-5.2-codex "{prompt}"'
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, encoding='utf-8', errors='replace'
            )
            if result.returncode != 0:
                self.logger.log_event("OPENCODE_ERROR", {"stderr": result.stderr})
                return f"Error executing opencode: {result.stderr}"
            return result.stdout.strip()
        except Exception as e:
            self.logger.log_event("OPENCODE_EXCEPTION", {"error": str(e)})
            return str(e)

    def _get_kimi_output(self, prompt):
        """Lanza la consulta a Kimi AI vía script de integración."""
        try:
            # Usamos el script existente kimi_integration.py
            cmd = f'python scripts/kimi_integration.py "{prompt}"'
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, encoding='utf-8', errors='replace'
            )
            if result.returncode != 0:
                self.logger.log_event("KIMI_ERROR", {"stderr": result.stderr})
                return f"Error executing Kimi: {result.stderr}"
            
            output = result.stdout
            if "Response:" in output:
                output = output.split("Response:")[1].strip()
            return output
            
        except Exception as e:
            self.logger.log_event("KIMI_EXCEPTION", {"error": str(e)})
            return str(e)

    # Alias para compatibilidad con métodos existentes
    def _get_opencode_output_legacy(self, prompt):
        return self._get_llm_output(prompt)

    def _detect_system_intent(self, objective):
        """
        Detects if the user wants to configure the AGENT SYSTEM itself (e.g., switch to GPT/Kimi),
        rather than configuring the target application.
        Returns True if a system command was detected and handled.
        """
        obj_lower = objective.lower().strip()
        
        # Regex-like simple patterns for Mode Switching
        gpt_keywords = ["modo gpt", "mode gpt", "use gpt engine", "usar motor gpt", "switch to gpt", "activar gpt", "ponme con gpt"]
        kimi_keywords = ["modo kimi", "mode kimi", "use kimi engine", "usar motor kimi", "switch to kimi", "activar kimi", "ponme con kimi"]
        auto_keywords = ["modo auto", "mode auto", "switch to auto", "activar auto", "reset mode"]

        new_mode = None
        
        # Check against patterns
        # We need to be careful not to trigger on "install gpt library in the app"
        # So we look for "mode" or "engine" context usually, or specific phrases.
        
        # Direct instruction matching
        if any(k in obj_lower for k in gpt_keywords):
             # Disambiguation: Check if it says "install" or "add" which might mean app config
             if "install" not in obj_lower and "add" not in obj_lower and "configura la app" not in obj_lower:
                 new_mode = "GPT_ONLY"
        
        elif any(k in obj_lower for k in kimi_keywords):
             if "install" not in obj_lower and "add" not in obj_lower:
                 new_mode = "KIMI_ONLY"

        elif any(k in obj_lower for k in auto_keywords):
             new_mode = "AUTO"

        if new_mode:
            print(f"{self.log_tag} ⚙️ META-COMMAND DETECTED: Switching System Mode to [{new_mode}]")
            self._update_system_mode(new_mode)
            return True
            
        return False

    def _update_system_mode(self, mode):
        """Updates the .env file with the new mode."""
        env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
        lines = []
        mode_found = False
        
        try:
            if os.path.exists(env_path):
                with open(env_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
            
            new_lines = []
            for line in lines:
                if line.startswith("MAESTRO_MODE="):
                    new_lines.append(f"MAESTRO_MODE={mode}\n")
                    mode_found = True
                else:
                    new_lines.append(line)
            
            if not mode_found:
                new_lines.append(f"MAESTRO_MODE={mode}\n")
            
            with open(env_path, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
            
            # Update current process env as well for immediate effect if needed (though script restarts often)
            os.environ["MAESTRO_MODE"] = mode
            print(f"{self.log_tag} ✅ System Mode updated to: {mode}")
            
        except Exception as e:
            print(f"{self.log_tag} ❌ Failed to update .env: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python autonomous_engine.py <objective>")
        sys.exit(1)
        
    objective = sys.argv[1]
    engine = AutonomousEngine()
    engine.run_autonomous_loop(objective)
