---
name: continuous-processing
description: Run continuous task processing using Ralph Wiggum loop
trigger: /continuous-processing
---

# Continuous Processing Skill

This skill enables continuous, autonomous task processing using Claude Code's loop mechanism for Silver Tier automation.

## What This Skill Does

1. Starts a continuous processing loop
2. Monitors Needs_Action folder automatically
3. Processes tasks as they appear
4. Runs until manually stopped or all tasks complete
5. Provides true 24/7 automation capability

## Usage

**Start continuous processing:**
```bash
/continuous-processing
```

**Or use the built-in loop command:**
```bash
/loop 5m /process-tasks
```

This runs `/process-tasks` every 5 minutes automatically.

## Instructions for Claude

When this skill is invoked:

1. **Initialize Continuous Mode**
   - Log start time
   - Set up monitoring
   - Prepare for long-running operation

2. **Main Processing Loop**
   ```
   LOOP:
     1. Check Needs_Action folder
     2. If tasks found:
        - Run /process-tasks
        - Update Dashboard
        - Log activity
     3. Check Pending_Approval folder
     4. If approvals found:
        - Run /process-approvals
        - Execute approved actions
     5. Wait [interval] seconds
     6. REPEAT
   ```

3. **Monitoring**
   - Track tasks processed
   - Log errors
   - Update Dashboard with loop status
   - Alert on failures

4. **Completion Conditions**
   - Manual stop (Ctrl+C)
   - Max iterations reached
   - Critical error encountered
   - User-defined completion signal

## Silver Tier Automation Setup

### Option 1: Using /loop Command (Recommended)

```bash
# Start Claude Code
claude

# Run continuous processing every 5 minutes
/loop 5m /process-tasks

# This will:
# - Check for tasks every 5 minutes
# - Process automatically
# - Keep running until you stop it
```

### Option 2: Using Ralph Wiggum Pattern

```bash
# Start Claude Code
claude

# Run with completion promise
/ralph-loop "Process all tasks in Needs_Action until folder is empty" \
  --completion-promise "ALL_TASKS_COMPLETE" \
  --max-iterations 100
```

### Option 3: Scheduled via Cron/Task Scheduler

**Linux/Mac (crontab):**
```bash
# Edit crontab
crontab -e

# Add line to run every hour
0 * * * * cd /path/to/project && claude --execute "/process-tasks" >> /path/to/logs/cron.log 2>&1
```

**Windows (Task Scheduler):**
```powershell
# Create scheduled task
$action = New-ScheduledTaskAction -Execute "claude" -Argument "/process-tasks" -WorkingDirectory "E:\Farhan-work\Hackathon\Agentic-Autonomous-Employee"
$trigger = New-ScheduledTaskTrigger -Once -At 9am -RepetitionInterval (New-TimeSpan -Hours 1)
Register-ScheduledTask -TaskName "AI Employee Processing" -Action $action -Trigger $trigger
```

## Full Automation Workflow

**Terminal 1 - Filesystem Watcher:**
```bash
python watchers/filesystem_watcher.py
# Runs 24/7, detects file drops
```

**Terminal 2 - Gmail Watcher:**
```bash
python watchers/gmail_watcher.py
# Runs 24/7, monitors inbox
```

**Terminal 3 - Continuous Processing:**
```bash
claude
/loop 5m /process-tasks
# Processes tasks every 5 minutes automatically
```

**Result:** Fully autonomous AI Employee!

## Monitoring Continuous Processing

**Check Dashboard:**
```bash
# View current status
cat AI_Employee_Vault/Dashboard.md
```

**Watch Logs:**
```bash
# Monitor processing activity
tail -f AI_Employee_Vault/Logs/orchestrator.log
```

**Check Task Queue:**
```bash
# See pending tasks
ls AI_Employee_Vault/Needs_Action/
```

## Safety Features

- **Max Iterations**: Prevents infinite loops
- **Error Handling**: Graceful degradation on failures
- **Logging**: Complete audit trail
- **Manual Override**: Can stop anytime with Ctrl+C
- **Approval Workflow**: Sensitive actions still require human approval

## Performance Tuning

**Adjust Check Interval:**
```bash
# Fast (every 2 minutes)
/loop 2m /process-tasks

# Standard (every 5 minutes)
/loop 5m /process-tasks

# Slow (every 15 minutes)
/loop 15m /process-tasks
```

**Balance:**
- Faster = More responsive, higher API usage
- Slower = Lower costs, less responsive

## Output Format

**Startup:**
```
Continuous processing started
Mode: Loop every 5 minutes
Monitoring: AI_Employee_Vault/Needs_Action
Press Ctrl+C to stop

[Loop 1] Checking for tasks...
[Loop 1] Found 2 tasks, processing...
[Loop 1] Complete. Next check in 5 minutes.

[Loop 2] Checking for tasks...
[Loop 2] No tasks found. Next check in 5 minutes.
```

## Integration with Other Skills

This skill orchestrates:
- `/process-tasks` - Main task processing
- `/process-approvals` - Approval workflow
- `/create-plan` - Complex task planning
- `/send-email` - Email actions
- `/post-linkedin` - Social media posts

## Silver Tier Complete Setup

With continuous processing, your Silver Tier is fully automatic:

1. ✅ Watchers detect new inputs (files, emails)
2. ✅ Tasks created automatically
3. ✅ Continuous loop processes tasks
4. ✅ Plans created for complex tasks
5. ✅ Approvals requested for sensitive actions
6. ✅ Dashboard updated in real-time
7. ✅ Complete audit trail

**True 24/7 autonomous operation achieved!**
