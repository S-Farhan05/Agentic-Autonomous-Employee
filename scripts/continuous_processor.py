#!/usr/bin/env python3
"""
Continuous Processor - Automatically invokes Qwen Code every N minutes

Silver Tier: This script runs continuously and invokes Qwen Code to process
tasks at regular intervals, providing full automation.

This is the "heartbeat" of your AI Employee system.
"""

import time
import subprocess
import logging
from pathlib import Path
from datetime import datetime

class ContinuousProcessor:
    """Continuously process tasks with Qwen Code"""

    def __init__(self, vault_path: str, check_interval: int = 120):
        """
        Initialize the continuous processor

        Args:
            vault_path: Path to the Obsidian vault
            check_interval: Seconds between Qwen invocations (default: 120 = 2 minutes)
        """
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.approved = self.vault_path / 'Approved'
        self.check_interval = check_interval
        self.logger = self._setup_logger()
        self.last_task_count = 0

    def _setup_logger(self):
        """Setup logging for continuous processor"""
        logger = logging.getLogger('ContinuousProcessor')
        logger.setLevel(logging.INFO)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # File handler
        log_dir = self.vault_path / 'Logs'
        log_dir.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(
            log_dir / 'continuous_processor.log'
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
        """Count pending tasks in Needs_Action and Approved folders"""
        needs_action_count = 0
        approved_count = 0

        if self.needs_action.exists():
            needs_action_count = len(list(self.needs_action.glob('*.md')))

        if self.approved.exists():
            approved_count = len(list(self.approved.glob('*.md')))

        return needs_action_count, approved_count

    def invoke_qwen(self, task_count, approved_count):
        """Automatically invoke Qwen Code to process tasks"""
        self.logger.info("="*60)
        self.logger.info(f"PROCESSING CYCLE: {task_count} tasks + {approved_count} approvals")
        self.logger.info("="*60)
        self.logger.info("Invoking Qwen Code...")

        try:
            # Create a comprehensive prompt with explicit instructions
            prompt = f"""You are the AI Employee brain. Process tasks autonomously.

CURRENT STATUS:
- {task_count} tasks in Needs_Action folder
- {approved_count} approved actions ready to execute

YOUR TASKS (execute in order):

1. READ Company Handbook: AI_Employee_Vault/Company_Handbook.md
   - Understand decision authority levels
   - Key rule: Sending emails requires human approval

2. PROCESS Needs_Action FOLDER:
   - Read all .md files in AI_Employee_Vault/Needs_Action/
   - For each EMAIL task (type: email):
     * Determine if reply needed (greeting/question/request = yes)
     * If reply needed: CREATE approval request in Pending_Approval/
     * Draft professional response
     * Move original task to Done/
   
3. PROCESS Approved FOLDER:
   - Read files in AI_Employee_Vault/Approved/
   - Execute approved email sends via Gmail API
   - Log actions to Logs/
   - Move completed to Done/

4. UPDATE Dashboard.md with all activities

IMPORTANT: Create files directly. Use write_file tool for all file operations.

Start processing now."""

            # Write prompt to temporary file in vault root
            prompt_file = self.vault_path / '.processor_prompt.md'
            prompt_file.write_text(prompt, encoding='utf-8')

            # Invoke Qwen Code - read prompt from file using @ syntax
            # Use -y flag for auto-approval of tool calls (file writes, etc.)
            cmd = f'qwen -y "@{prompt_file}"'

            result = subprocess.run(
                cmd,
                shell=True,
                cwd=str(self.vault_path.parent),
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )

            # Log full output for debugging
            self.logger.info(f"Qwen output: {result.stdout[:1000]}")
            if result.stderr:
                self.logger.warning(f"Qwen stderr: {result.stderr[:500]}")

            # Clean up prompt file
            if prompt_file.exists():
                prompt_file.unlink()

            if result.returncode == 0:
                self.logger.info("Qwen Code processing completed successfully")
                self.logger.info("="*60)
                return True
            else:
                self.logger.warning(f"Qwen Code returned code {result.returncode}")
                return False

        except subprocess.TimeoutExpired:
            self.logger.error("Qwen Code processing timed out (5 min)")
            return False
        except Exception as e:
            self.logger.error(f"Error invoking Qwen Code: {e}")
            return False

    def run(self):
        """Main continuous processing loop"""
        self.logger.info("="*60)
        self.logger.info("CONTINUOUS PROCESSOR STARTED")
        self.logger.info("="*60)
        self.logger.info(f"Monitoring: {self.needs_action}")
        self.logger.info(f"Processing interval: {self.check_interval} seconds ({self.check_interval/60:.1f} minutes)")
        self.logger.info(f"Vault path: {self.vault_path}")
        self.logger.info("")
        self.logger.info("Qwen Code will be invoked automatically to process tasks.")
        self.logger.info("Full automation enabled - no manual intervention needed.")
        self.logger.info("Press Ctrl+C to stop.")
        self.logger.info("="*60)

        try:
            while True:
                task_count, approved_count = self.count_tasks()
                total_work = task_count + approved_count

                # Process if there's work to do
                if total_work > 0:
                    self.logger.info(f"Found {task_count} task(s) + {approved_count} approval(s) to process")

                    # Invoke Qwen to process tasks
                    success = self.invoke_qwen(task_count, approved_count)

                    if success:
                        # Wait a moment for processing to complete
                        time.sleep(10)

                        # Check if tasks were processed
                        new_task_count, new_approved_count = self.count_tasks()
                        if new_task_count < task_count or new_approved_count < approved_count:
                            self.logger.info(f"Processing successful. Remaining: {new_task_count} tasks + {new_approved_count} approvals")
                        else:
                            self.logger.info("Qwen invoked. Check Dashboard for results.")

                        self.last_task_count = new_task_count + new_approved_count
                    else:
                        self.logger.warning("Auto-processing failed, will retry on next cycle")

                else:
                    if self.last_task_count != 0:
                        self.logger.info("All tasks processed. Waiting for new tasks...")
                    self.last_task_count = 0

                # Wait before next cycle
                self.logger.info(f"Next processing cycle in {self.check_interval} seconds...")
                time.sleep(self.check_interval)

        except KeyboardInterrupt:
            self.logger.info("")
            self.logger.info("="*60)
            self.logger.info("Continuous processor stopped by user")
            self.logger.info("="*60)


if __name__ == '__main__':
    import sys

    # Get vault path from command line or use default
    if len(sys.argv) > 1:
        vault_path = sys.argv[1]
    else:
        vault_path = Path(__file__).parent.parent / 'AI_Employee_Vault'

    # Optional: specify check interval in seconds (default: 120 = 2 minutes)
    check_interval = int(sys.argv[2]) if len(sys.argv) > 2 else 120

    # Create and run continuous processor
    processor = ContinuousProcessor(str(vault_path), check_interval)
    processor.run()
