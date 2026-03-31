#!/usr/bin/env python3
"""
Orchestrator - Automatically invokes Claude Code when tasks appear

Bronze Tier Enhanced: This orchestrator monitors for tasks and automatically
invokes Claude Code to process them, making the system fully autonomous.

This is the "brain" that keeps your AI Employee running 24/7.
"""

import time
import subprocess
import logging
from pathlib import Path
from datetime import datetime

class Orchestrator:
    """Main orchestrator for AI Employee automation"""

    def __init__(self, vault_path: str, check_interval: int = 60):
        """
        Initialize the orchestrator

        Args:
            vault_path: Path to the Obsidian vault
            check_interval: Seconds between checks (default: 60)
        """
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.check_interval = check_interval
        self.logger = self._setup_logger()
        self.last_task_count = 0

    def _setup_logger(self):
        """Setup logging for orchestrator"""
        logger = logging.getLogger('Orchestrator')
        logger.setLevel(logging.INFO)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # File handler
        log_dir = self.vault_path / 'Logs'
        log_dir.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(
            log_dir / 'orchestrator.log'
        )
        file_handler.setLevel(logging.DEBUG)

        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        return logger

    def count_tasks(self):
        """Count pending tasks in Needs_Action folder"""
        if not self.needs_action.exists():
            return 0

        tasks = list(self.needs_action.glob('*.md'))
        return len(tasks)

    def invoke_claude(self, task_count):
        """Automatically invoke Claude Code to process tasks"""
        self.logger.info("="*60)
        self.logger.info(f"PROCESSING: {task_count} task(s) detected in Needs_Action")
        self.logger.info("="*60)
        self.logger.info("Invoking Claude Code...")

        try:
            # Create a prompt file for Claude to process
            prompt = f"""Please process all tasks in the Needs_Action folder.

Read the Company_Handbook.md for rules, then:
1. Analyze each task in AI_Employee_Vault/Needs_Action/
2. For simple tasks: process and move to Done
3. For complex tasks: create a Plan in Plans/ folder
4. Update Dashboard.md with results
5. Log all actions

Run the /process-tasks skill to complete this.
"""

            # Write prompt to temporary file
            prompt_file = self.vault_path / '.orchestrator_prompt.txt'
            prompt_file.write_text(prompt, encoding='utf-8')

            # Invoke Claude Code with the prompt
            # Using echo to pipe the command into claude
            cmd = f'echo "/process-tasks" | claude'

            result = subprocess.run(
                cmd,
                shell=True,
                cwd=self.vault_path.parent,
                capture_output=True,
                text=True,
                timeout=180  # 3 minute timeout
            )

            # Clean up prompt file
            if prompt_file.exists():
                prompt_file.unlink()

            if result.returncode == 0 or "process" in result.stdout.lower():
                self.logger.info("Claude Code invoked successfully")
                self.logger.info("="*60)
                return True
            else:
                self.logger.warning(f"Claude Code returned code {result.returncode}")
                self.logger.debug(f"Output: {result.stdout[:200]}")
                return False

        except subprocess.TimeoutExpired:
            self.logger.error("Claude Code processing timed out (3 min)")
            return False
        except Exception as e:
            self.logger.error(f"Error invoking Claude Code: {e}")
            self.logger.info("Falling back to notification mode...")
            self._notify_manual_processing(task_count)
            return False

    def _notify_manual_processing(self, task_count):
        """Fallback: Notify user to process manually"""
        self.logger.info("")
        self.logger.info("FALLBACK MODE: Please process manually")
        self.logger.info("  1. Open terminal")
        self.logger.info("  2. Run: claude")
        self.logger.info("  3. Execute: /process-tasks")
        self.logger.info("="*60)

    def _update_dashboard_notification(self, task_count):
        """Add notification to dashboard"""
        try:
            dashboard = self.vault_path / 'Dashboard.md'
            if dashboard.exists():
                content = dashboard.read_text(encoding='utf-8')

                # Add alert if not already present
                alert_text = f"- WARNING: {task_count} task(s) waiting in Needs_Action - Run /process-tasks"
                if alert_text not in content:
                    # Update alerts section
                    if "## Alerts" in content:
                        content = content.replace(
                            "*No alerts*",
                            alert_text
                        )
                        dashboard.write_text(content, encoding='utf-8')
                        self.logger.debug("Dashboard notification added")
        except Exception as e:
            self.logger.debug(f"Could not update dashboard: {e}")

    def run(self):
        """Main orchestrator loop"""
        self.logger.info("="*60)
        self.logger.info("AI EMPLOYEE ORCHESTRATOR STARTED")
        self.logger.info("="*60)
        self.logger.info(f"Monitoring: {self.needs_action}")
        self.logger.info(f"Check interval: {self.check_interval} seconds")
        self.logger.info(f"Vault path: {self.vault_path}")
        self.logger.info("")
        self.logger.info("Orchestrator will AUTOMATICALLY invoke Claude when tasks appear.")
        self.logger.info("Full automation enabled - no manual intervention needed.")
        self.logger.info("Press Ctrl+C to stop.")
        self.logger.info("="*60)

        try:
            while True:
                task_count = self.count_tasks()

                # Only process if there are new tasks
                if task_count > 0 and task_count != self.last_task_count:
                    self.logger.info(f"Found {task_count} task(s) in Needs_Action folder")

                    # Automatically invoke Claude to process tasks
                    success = self.invoke_claude(task_count)

                    if success:
                        # Wait a moment for processing to complete
                        time.sleep(5)

                        # Check if tasks were processed
                        new_count = self.count_tasks()
                        if new_count < task_count:
                            self.logger.info(f"Processing successful. Tasks remaining: {new_count}")
                        else:
                            self.logger.info("Claude invoked. Check Dashboard for results.")

                        self.last_task_count = new_count
                    else:
                        self.logger.warning("Auto-processing failed, will retry on next check")
                        # Don't update last_task_count so it retries

                elif task_count == 0:
                    if self.last_task_count != 0:
                        self.logger.info("All tasks processed. Waiting for new tasks...")
                    self.last_task_count = 0

                # Wait before next check
                time.sleep(self.check_interval)

        except KeyboardInterrupt:
            self.logger.info("")
            self.logger.info("="*60)
            self.logger.info("Orchestrator stopped by user")
            self.logger.info("="*60)


if __name__ == '__main__':
    import sys

    # Get vault path from command line or use default
    if len(sys.argv) > 1:
        vault_path = sys.argv[1]
    else:
        vault_path = Path(__file__).parent.parent / 'AI_Employee_Vault'

    # Optional: specify check interval
    check_interval = int(sys.argv[2]) if len(sys.argv) > 2 else 60

    # Create and run orchestrator
    orchestrator = Orchestrator(str(vault_path), check_interval)
    orchestrator.run()
