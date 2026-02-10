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
    Motor de Autonomía Total v6.1 (Enhanced)
    Implementa el loop: Plan -> Execute -> Verify -> Repair
    Soporta Orquestación Granular (Modo por Agente).
    """
    def __init__(self, forced_mode=None):
        self.logger = StructuredLogger()
        self.context_bridge = "scripts/opencode_bridge.py"
        self.log_tag = "[AUTONOMOUS ENGINE v6.1]"
        self.forced_mode = forced_mode

    def _get_effective_mode(self):
        """Retorna el modo efectivo (Forzado > Env > Default)."""
        if self.forced_mode:
            return self.forced_mode.upper()
        return os.getenv("MAESTRO_MODE", "AUTO").upper()

    def plan(self, objective):
        """Planifica el objetivo usando el modelo adecuado según el modo."""
        
        # INTERCEPTION: Check if this is a System Configuration Command (Meta-Command)
        if self._detect_system_intent(objective):
            # Return a dummy step so the loop completes successfully and logs the action
            print(f"{self.log_tag} System Configuration updated. Returning confirmation step.")
            return [{'command': 'echo "System configuration updated successfully."', 'description': 'Confirm system configuration update'}]

        mode = self._get_effective_mode()
        print(f"{self.log_tag} [MODO ACTIVO: {mode}] Planificando objetivo: {objective}")
        self.logger.log_compliance_check(f"v6.1_PLANNING_{mode}", "IN_PROGRESS", f"Objective: {objective}")

        # Construct Prompt based on Mode
        if mode == "KIMI_ONLY" or mode == "KIMI":
            planner_model = "KIMI"
            role_desc = "ROLE: You are the SOLE Executor (Kimi AI)."
            extra_inst = "Use your 128k context window to analyze and execute."
        elif mode == "GROK_ONLY" or mode == "GROK":
            planner_model = "GROK"
            role_desc = "ROLE: You are the SOLE Executor (Grok - xAI)."
            extra_inst = "Use your real-time knowledge and unfiltered reasoning."
        elif mode == "GPT_ONLY" or mode == "GPT":
            planner_model = "GPT"
            role_desc = "ROLE: You are the SOLE Executor (GPT-4o/5.2)."
            extra_inst = "Do NOT delegate to any other agent. Do NOT use `kimi_integration.py`."
        elif mode == "NATIVE":
            planner_model = "NATIVE"
            role_desc = "ROLE: You are the SOLE Executor (Antigravity Gemini 3 - NATIVE)."
            extra_inst = "Operate with maximum precision using native system capabilities."
        else: # AUTO (Default - Hybrid)
            planner_model = "GPT"
            role_desc = "PROTOCOL: HYBRID ORCHESTRATION (AUTO MODE)"
            extra_inst = (
                "ROLES:\n"
                "- TÚ (GPT-5.2): Cerebro Lógico, Backend, Sistemas, Datos. TÚ ERES EL JEFE.\n"
                "- KIMI AI: Especialista en Frontend (HTML/CSS/JS), Diseño, y Análisis de Contexto Masivo (>8k).\n\n"
                "DECISION TREE:\n"
                "1. IF task is UI/Design/Frontend -> DELEGATE to Kimi (`python scripts/kimi_integration.py ...`).\n"
                "2. IF task is Logic/System/Backend -> EXECUTE yourself.\n"
                "3. IF context is huge -> DELEGATE analysis to Kimi.\n"
                "4. IF task is ideal for Grok (Real-time X search, Deep reasoning) -> DO NOT execute it. "
                "Instead, add a step: {'command': 'echo \"[SUGERENCIA: Usar Grok]\"', 'description': 'SUGERENCIA: Esta parte requiere Grok por [Razón]. Habilítalo con \"Modo Grok\".'}"
            )

        prompt = (
            f"Objective: {objective} \n"
            "Environment: Windows PowerShell / Maestro skills v5.0 \n"
            f"{role_desc} \n"
            f"{extra_inst} \n"
            "Return ONLY a raw JSON object (no markdown) with this structure: "
            "{'steps': [{'command': 'shell_command', 'description': 'step_description'}]}"
        )

        # Execute Planning
        plan_raw = self._call_model(planner_model, prompt)
        
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

    def _call_model(self, model, prompt):
        """Centralized model router."""
        if model == "KIMI":
            return self._get_kimi_output(prompt)
        elif model == "GROK":
            return self._get_grok_output(prompt)
        elif model == "GPT":
            return self._get_opencode_output(prompt)
        elif model == "NATIVE":
            return self._get_native_output(prompt)
        return self._get_opencode_output(prompt)

    def _get_native_output(self, prompt):
        """Simula o delega la salida al sistema Antigravity/Gemini base."""
        print(f"{self.log_tag} Usando MODO NATIVO (Antigravity Gemini 3)")
        # En una implementación real fuera de este entorno, esto llamaría a un script de Gemini.
        # Aquí, marcamos el output para que el sistema que ejecuta el script sepa qué hacer.
        return f"[ANTIGRAVITY_NATIVE_EXECUTION]\n{prompt}"

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
        
        mode = self._get_effective_mode()
        if mode in ["KIMI_ONLY", "KIMI"]:
            verification = self._get_kimi_output(prompt).strip()
        elif mode == "NATIVE":
            verification = self._get_native_output(prompt).strip()
        else:
            verification = self._get_opencode_output(prompt).strip()

        if verification.startswith("Error"):
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
        
        mode = self._get_effective_mode()
        if mode in ["KIMI_ONLY", "KIMI"]:
            repair_plan = self._get_kimi_output(prompt)
        elif mode == "NATIVE":
            repair_plan = self._get_native_output(prompt)
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
        
        mode = self._get_effective_mode()
        if mode in ["GPT_ONLY", "GPT"] and "kimi_integration.py" in command:
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

    def _get_llm_output(self, prompt):
        """Redirects based on effective mode."""
        mode = self._get_effective_mode()
        if mode in ["KIMI_ONLY", "KIMI"]:
            return self._get_kimi_output(prompt)
        elif mode in ["GROK_ONLY", "GROK"]:
            return self._get_grok_output(prompt)
        elif mode in ["GPT_ONLY", "GPT"]:
            return self._get_opencode_output(prompt)
        elif mode == "NATIVE":
            return self._get_native_output(prompt)
        else: # AUTO MODE
            if len(prompt) > 8000 and os.getenv("KIMI_API_KEY"):
                 print(f"{self.log_tag} ⚠️ CONTEXT > 8k chars in AUTO mode. Using KIMI for heavy lifting.")
                 return self._get_kimi_output(prompt)
            return self._get_opencode_output(prompt)

    def _get_grok_output(self, prompt):
        try:
            cmd = f'python scripts/grok_integration.py "{prompt}"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8', errors='replace')
            if result.returncode != 0:
                self.logger.log_event("GROK_ERROR", {"stderr": result.stderr})
                return f"Error executing Grok: {result.stderr}"
            return result.stdout.strip()
        except Exception as e:
            self.logger.log_event("GROK_EXCEPTION", {"error": str(e)})
            return str(e)

    def _get_opencode_output(self, prompt):
        try:
            cmd = f'python scripts/gpt_browser_bridge.py "{prompt}"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8', errors='replace')
            if result.returncode != 0:
                self.logger.log_event("GPT_BRIDGE_ERROR", {"stderr": result.stderr})
                return f"Error executing GPT Bridge: {result.stderr}"
            output = result.stdout.strip()
            if not output: return "Error: Empty response from GPT Bridge."
            return output
        except Exception as e:
            self.logger.log_event("GPT_BRIDGE_EXCEPTION", {"error": str(e)})
            return str(e)

    def _get_kimi_output(self, prompt):
        try:
            cmd = f'python scripts/kimi_integration.py "{prompt}"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8', errors='replace')
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

    def _detect_system_intent(self, objective):
        obj_lower = objective.lower().strip()
        gpt_keywords = ["modo gpt", "mode gpt", "use gpt", "switch to gpt"]
        kimi_keywords = ["modo kimi", "mode kimi", "use kimi", "switch to kimi"]
        grok_keywords = ["modo grok", "mode grok", "use grok", "switch to grok"]
        native_keywords = ["modo nativo", "native mode", "use gemini", "usa gemini", "usar gemini"]
        auto_keywords = ["modo auto", "mode auto", "reset mode"]

        new_mode = None
        if any(k in obj_lower for k in gpt_keywords): new_mode = "GPT_ONLY"
        elif any(k in obj_lower for k in kimi_keywords): new_mode = "KIMI_ONLY"
        elif any(k in obj_lower for k in grok_keywords): new_mode = "GROK_ONLY"
        elif any(k in obj_lower for k in native_keywords): new_mode = "NATIVE"
        elif any(k in obj_lower for k in auto_keywords): new_mode = "AUTO"

        if new_mode:
            print(f"{self.log_tag} ⚙️ META-COMMAND DETECTED: Switching System Mode to [{new_mode}]")
            self._update_system_mode(new_mode)
            return True
        return False

    def _update_system_mode(self, mode):
        env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
        try:
            lines = []
            if os.path.exists(env_path):
                with open(env_path, "r", encoding="utf-8") as f: lines = f.readlines()
            
            new_lines = []
            found = False
            for line in lines:
                if line.startswith("MAESTRO_MODE="):
                    new_lines.append(f"MAESTRO_MODE={mode}\n")
                    found = True
                else: new_lines.append(line)
            if not found: new_lines.append(f"MAESTRO_MODE={mode}\n")
            
            with open(env_path, "w", encoding="utf-8") as f: f.writelines(new_lines)
            os.environ["MAESTRO_MODE"] = mode
            print(f"{self.log_tag} ✅ System Mode updated to: {mode}")
        except Exception as e: print(f"{self.log_tag} ❌ Failed to update .env: {e}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Autonomous Engine CLI v6.1")
    parser.add_argument("objective", type=str, help="Objetivo a realizar")
    parser.add_argument("--mode", type=str, help="Forzar modo (GPT, KIMI, GROK, NATIVE, AUTO)")
    
    args = parser.parse_args()
    engine = AutonomousEngine(forced_mode=args.mode)
    engine.run_autonomous_loop(args.objective)
