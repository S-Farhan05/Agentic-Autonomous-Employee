"# AI Employee - Bronze Tier Implementation

A local-first Personal AI Employee built with Claude Code and Obsidian. This Bronze Tier implementation provides the foundational infrastructure for autonomous task processing.

## Overview

This project implements the Bronze Tier requirements from the Personal AI Employee Hackathon:
- ✅ Obsidian vault with Dashboard.md and Company_Handbook.md
- ✅ File system watcher for monitoring drop folder
- ✅ Claude Code integration for reading/writing to vault
- ✅ Basic folder structure: /Inbox, /Needs_Action, /Done
- ✅ Agent Skill for task processing

## Architecture

```
┌─────────────────────────────────────────┐
│         External Input (Files)          │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│      File System Watcher (Python)       │
│  Monitors: AI_Employee_Vault/Inbox/     │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│         Obsidian Vault (Local)          │
│  /Inbox → /Needs_Action → /Done         │
│  Dashboard.md | Company_Handbook.md     │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│      Claude Code (Reasoning Engine)     │
│  Skill: /process-tasks                  │
│  Read → Analyze → Act → Update          │
└─────────────────────────────────────────┘
```

## Prerequisites

- **Python**: 3.13 or higher
- **Claude Code**: Active subscription or free tier
- **Obsidian**: v1.10.6+ (optional, for GUI viewing)

## Installation

### 1. Navigate to Project Directory

```bash
cd E:\Farhan-work\Hackathon\Agentic-Autonomous-Employee
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Verify Folder Structure

The following structure should exist:
```
AI_Employee_Vault/
├── Inbox/              # Drop files here to trigger processing
├── Needs_Action/       # Tasks waiting to be processed
├── Done/               # Completed tasks
├── Plans/              # Multi-step task plans
├── Logs/               # System logs
├── Pending_Approval/   # Tasks requiring human approval
├── Approved/           # Approved tasks ready for execution
├── Rejected/           # Rejected tasks
├── Dashboard.md        # Main status dashboard
└── Company_Handbook.md # AI behavior rules
```

## Usage

### Starting the File System Watcher

The watcher monitors the Inbox folder and creates action files when new files are dropped.

```bash
# Start the watcher
python watchers/filesystem_watcher.py
```

The watcher will:
1. Monitor `AI_Employee_Vault/Inbox/` for new files
2. Copy files to `Needs_Action/` with `FILE_` prefix
3. Create metadata `.md` files describing each file
4. Log all activities to `Logs/filesystem_watcher.log`

### Processing Tasks with Claude Code

Once files are in the Needs_Action folder, use Claude Code to process them:

```bash
# Start Claude Code
claude

# In Claude Code, run the skill
/process-tasks
```

Claude will:
1. Read Company_Handbook.md for rules
2. Process all tasks in Needs_Action/
3. Execute auto-approved actions
4. Create approval requests for sensitive actions
5. Update Dashboard.md
6. Move completed tasks to Done/

### Viewing the Dashboard

Open `AI_Employee_Vault/Dashboard.md` in:
- **Obsidian**: For rich markdown viewing with links
- **Any text editor**: For quick status checks
- **Claude Code**: Ask Claude to read and summarize it

## Testing the System

### Test 1: File Drop

1. Start the watcher:
   ```bash
   python watchers/filesystem_watcher.py
   ```

2. Drop a test file into `AI_Employee_Vault/Inbox/`:
   ```bash
   echo "Test document content" > AI_Employee_Vault/Inbox/test.txt
   ```

3. Check `Needs_Action/` for the created files

### Test 2: Task Processing

1. Ensure test files are in `Needs_Action/`
2. Run Claude Code and execute `/process-tasks`
3. Check Dashboard.md for updates

## Configuration

### Customizing AI Behavior

Edit `AI_Employee_Vault/Company_Handbook.md` to:
- Add new rules
- Change priority levels
- Modify approval thresholds
- Define working hours

## Troubleshooting

### Watcher Not Starting

**Error**: `ModuleNotFoundError: No module named 'watchdog'`

**Solution**: Install dependencies
```bash
pip install watchdog
```

### Files Not Being Detected

**Check**:
1. Watcher is running (check console output)
2. Files are in correct folder (`Inbox/`)
3. Files are not hidden (don't start with `.` or `~`)
4. Check logs: `AI_Employee_Vault/Logs/filesystem_watcher.log`

## Next Steps (Silver Tier)

To upgrade to Silver Tier, add:
- Gmail watcher for email monitoring
- WhatsApp watcher for message monitoring
- MCP server for sending emails
- Human-in-the-loop approval workflow
- Scheduling via cron/Task Scheduler

## Security Notes

- All data stays local in the vault
- No credentials stored in plain text
- Logs contain audit trail of all actions
- Human approval required for sensitive actions

---

**Bronze Tier Status**: ✅ Complete

Built with Claude Code | Powered by Anthropic" 
