# Quick Start Guide

Get your AI Employee running in 5 minutes!

## Step 1: Install Dependencies (1 minute)

```bash
pip install -r requirements.txt
```

## Step 2: Test the File Watcher (2 minutes)

Open a terminal and start the watcher:

```bash
python watchers/filesystem_watcher.py
```

Keep this terminal open. You should see:
```
Starting FileSystemWatcher
Watching folder: E:\Farhan-work\Hackathon\Agentic-Autonomous-Employee\AI_Employee_Vault\Inbox
```

## Step 3: Drop a Test File (30 seconds)

Open another terminal and create a test file:

```bash
echo "This is a test document for my AI Employee" > AI_Employee_Vault/Inbox/test_document.txt
```

In the watcher terminal, you should see:
```
Processed new file: test_document.txt
```

Check the Needs_Action folder - you'll find:
- `FILE_test_document.txt` (the file itself)
- `FILE_test_document.txt.md` (metadata about the file)

## Step 4: Process Tasks with Claude (1 minute)

Open Claude Code:

```bash
claude
```

In Claude, run:

```
/process-tasks
```

Claude will:
- Read the Company_Handbook.md
- Process all tasks in Needs_Action
- Update Dashboard.md
- Move completed tasks to Done

## Step 5: View Results (30 seconds)

Check the Dashboard:

```bash
cat AI_Employee_Vault/Dashboard.md
```

Or open it in Obsidian for a better view.

## What's Next?

### Try These:

1. **Drop different file types**
   ```bash
   echo "Meeting notes" > AI_Employee_Vault/Inbox/meeting.txt
   echo "Invoice data" > AI_Employee_Vault/Inbox/invoice.txt
   ```

2. **Create custom tasks**
   - Create a `.md` file in Needs_Action with your own task
   - Use the EXAMPLE_welcome_task.md as a template

3. **Customize the handbook**
   - Edit `AI_Employee_Vault/Company_Handbook.md`
   - Add your own rules and priorities

4. **Monitor the logs**
   ```bash
   tail -f AI_Employee_Vault/Logs/filesystem_watcher.log
   ```

### Upgrade to Silver Tier:

Once comfortable with Bronze, add:
- Gmail watcher for email monitoring
- MCP server for sending emails
- Scheduling for automatic processing

## Troubleshooting

**Watcher not detecting files?**
- Make sure you're dropping files in the `Inbox` folder
- Check the watcher is still running
- Look at the logs in `AI_Employee_Vault/Logs/`

**Claude not finding files?**
- Make sure you're running Claude from the project root directory
- Try: `cd E:\Farhan-work\Hackathon\Agentic-Autonomous-Employee`

**Skill not working?**
- Verify `.claude/skills/process-tasks.md` exists
- Try restarting Claude Code

## Success Criteria

You've successfully completed Bronze Tier when:
- ✅ Watcher detects and processes dropped files
- ✅ Claude can read and process tasks
- ✅ Dashboard updates automatically
- ✅ Tasks move from Needs_Action to Done
- ✅ Logs show all activities

Congratulations! You now have a working AI Employee foundation.
