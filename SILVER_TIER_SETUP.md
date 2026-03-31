# Silver Tier Setup Guide

Complete guide to setting up and running your Silver Tier AI Employee with full automation.

## What's New in Silver Tier

Silver Tier adds:
- ✅ Gmail watcher for email monitoring
- ✅ WhatsApp watcher for message monitoring
- ✅ LinkedIn posting capability
- ✅ Email sending via MCP
- ✅ Human-in-the-loop approval workflow
- ✅ Multi-step plan creation
- ✅ Continuous processing with /loop
- ✅ Business goals tracking

## Prerequisites

### 1. Install Additional Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Google API libraries (Gmail)
- Playwright (WhatsApp automation)
- Existing dependencies (watchdog)

### 2. Install Playwright Browsers

```bash
playwright install chromium
```

### 3. Gmail API Setup

**a. Create Google Cloud Project:**
1. Go to https://console.cloud.google.com
2. Create new project: "AI Employee"
3. Enable Gmail API
4. Create OAuth 2.0 credentials
5. Download credentials.json

**b. Save Credentials:**
```bash
mkdir credentials
mv ~/Downloads/credentials.json credentials/
```

**c. First Run Authentication:**
```bash
python watchers/gmail_watcher.py
# Browser will open for Google login
# Grant permissions
# Token saved for future use
```

### 4. WhatsApp Web Setup

**First run requires QR code scan:**
```bash
python watchers/whatsapp_watcher.py
# Browser opens to WhatsApp Web
# Scan QR code with your phone
# Session saved for future use
```

## Silver Tier Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    INPUT SOURCES                        │
├──────────────┬──────────────┬──────────────┬───────────┤
│   Files      │    Gmail     │   WhatsApp   │  Manual   │
└──────┬───────┴──────┬───────┴──────┬───────┴─────┬─────┘
       │              │              │             │
       ▼              ▼              ▼             ▼
┌─────────────────────────────────────────────────────────┐
│                    WATCHERS (Auto)                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │   File   │  │  Gmail   │  │ WhatsApp │             │
│  │ Watcher  │  │ Watcher  │  │ Watcher  │             │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘             │
└───────┼─────────────┼─────────────┼────────────────────┘
        │             │             │
        └─────────────┴─────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│              NEEDS_ACTION FOLDER                        │
│  Tasks waiting for processing                           │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│         CONTINUOUS PROCESSING (Auto)                    │
│  Claude Code with /loop 5m /process-tasks               │
│                                                          │
│  Every 5 minutes:                                       │
│  1. Check Needs_Action                                  │
│  2. Process tasks                                       │
│  3. Create plans for complex tasks                      │
│  4. Create approval requests                            │
└──────────────────────┬──────────────────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
        ▼                             ▼
┌──────────────┐            ┌──────────────────┐
│ AUTO-APPROVE │            │ REQUIRES APPROVAL│
│    Tasks     │            │      Tasks       │
└──────┬───────┘            └────────┬─────────┘
       │                             │
       │                    ┌────────▼─────────┐
       │                    │ Human Reviews    │
       │                    │ Moves to Approved│
       │                    └────────┬─────────┘
       │                             │
       └─────────────┬───────────────┘
                     ▼
┌─────────────────────────────────────────────────────────┐
│              EXECUTION (Auto)                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │  Email   │  │ LinkedIn │  │Dashboard │             │
│  │   MCP    │  │   API    │  │  Update  │             │
│  └──────────┘  └──────────┘  └──────────┘             │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│                  DONE FOLDER                            │
│  Completed tasks with audit trail                      │
└─────────────────────────────────────────────────────────┘
```

## Running Silver Tier

### Full Automation Setup (4 Terminals)

**Terminal 1 - File Watcher:**
```bash
cd E:\Farhan-work\Hackathon\Agentic-Autonomous-Employee
python watchers/filesystem_watcher.py
```

**Terminal 2 - Gmail Watcher:**
```bash
cd E:\Farhan-work\Hackathon\Agentic-Autonomous-Employee
python watchers/gmail_watcher.py
```

**Terminal 3 - WhatsApp Watcher:**
```bash
cd E:\Farhan-work\Hackathon\Agentic-Autonomous-Employee
python watchers/whatsapp_watcher.py
```

**Terminal 4 - Continuous Processing:**
```bash
cd E:\Farhan-work\Hackathon\Agentic-Autonomous-Employee
claude
/loop 5m /process-tasks
```

### What Happens Now

**Fully Automatic Workflow:**

1. **Email arrives** → Gmail watcher detects → Creates task
2. **WhatsApp message** → WhatsApp watcher detects → Creates task
3. **File dropped** → File watcher detects → Creates task
4. **Every 5 minutes** → Claude processes all tasks automatically
5. **Simple tasks** → Processed and moved to Done
6. **Complex tasks** → Plan created in Plans/
7. **Sensitive actions** → Approval request in Pending_Approval/
8. **You approve** → Move to Approved/ → Executed automatically
9. **Dashboard** → Updated in real-time

## Available Skills

### Core Processing
- `/process-tasks` - Process all pending tasks
- `/process-approvals` - Execute approved actions
- `/create-plan` - Create multi-step plans
- `/continuous-processing` - Start continuous loop

### Actions
- `/send-email` - Send email via MCP
- `/post-linkedin` - Post to LinkedIn

### Monitoring
- Check Dashboard.md for status
- View Logs/ for audit trail
- Monitor Needs_Action/ for queue

## Approval Workflow

### How It Works

1. **Task Requires Approval:**
   - Claude creates file in Pending_Approval/
   - Dashboard shows alert

2. **You Review:**
   - Open file in Pending_Approval/
   - Read details and context
   - Decide: Approve or Reject

3. **Approve:**
   - Move file to Approved/
   - Next processing cycle executes it

4. **Reject:**
   - Move file to Rejected/
   - Logged and archived

### Example Approval Flow

```bash
# 1. Claude creates approval request
Pending_Approval/EMAIL_invoice_client_a.md

# 2. You review and approve
mv Pending_Approval/EMAIL_invoice_client_a.md Approved/

# 3. Next loop cycle (within 5 min)
# Claude detects approved file
# Sends email via MCP
# Logs action
# Moves to Done/

# 4. Check result
cat AI_Employee_Vault/Dashboard.md
# Shows: "Email sent to Client A - Invoice delivered"
```

## MCP Server Setup (Optional for Silver Tier)

### Email MCP

Create `mcp-config.json`:
```json
{
  "mcpServers": {
    "email": {
      "command": "node",
      "args": ["path/to/email-mcp/index.js"],
      "env": {
        "GMAIL_CREDENTIALS": "credentials/credentials.json"
      }
    }
  }
}
```

### LinkedIn API

Configure LinkedIn OAuth:
1. Create LinkedIn App
2. Get access token
3. Configure in MCP or direct API calls

## Monitoring & Maintenance

### Daily Checks

```bash
# View Dashboard
cat AI_Employee_Vault/Dashboard.md

# Check pending approvals
ls AI_Employee_Vault/Pending_Approval/

# View recent logs
tail -50 AI_Employee_Vault/Logs/orchestrator.log
```

### Weekly Maintenance

```bash
# Archive old Done tasks
mv AI_Employee_Vault/Done/* AI_Employee_Vault/Archive/$(date +%Y-%m)/

# Review Business Goals
vim AI_Employee_Vault/Business_Goals.md

# Check watcher health
ps aux | grep watcher
```

## Troubleshooting

### Gmail Watcher Issues

**Error: credentials.json not found**
```bash
# Download from Google Cloud Console
# Place in credentials/ folder
```

**Error: Token expired**
```bash
# Delete old token
rm credentials/token.pickle
# Re-run watcher to re-authenticate
python watchers/gmail_watcher.py
```

### WhatsApp Watcher Issues

**Error: QR code not scanning**
```bash
# Run with visible browser
# Edit whatsapp_watcher.py: headless=False
# Scan QR code manually
```

**Error: Session expired**
```bash
# Delete session and re-scan
rm -rf whatsapp_session/
python watchers/whatsapp_watcher.py
```

### Continuous Processing Issues

**Loop not running**
```bash
# Check if Claude Code is active
# Restart loop:
claude
/loop 5m /process-tasks
```

## Performance Tuning

### Adjust Check Intervals

**Faster (more responsive, higher costs):**
```bash
# Watchers: Check every 30 seconds
python watchers/gmail_watcher.py AI_Employee_Vault 30

# Processing: Every 2 minutes
/loop 2m /process-tasks
```

**Slower (lower costs, less responsive):**
```bash
# Watchers: Check every 5 minutes
python watchers/gmail_watcher.py AI_Employee_Vault 300

# Processing: Every 15 minutes
/loop 15m /process-tasks
```

## Silver Tier Complete Checklist

- [ ] All dependencies installed
- [ ] Gmail API configured and authenticated
- [ ] WhatsApp session created
- [ ] Business_Goals.md customized
- [ ] All 3 watchers running
- [ ] Continuous processing active
- [ ] Test file drop → processed
- [ ] Test email → task created
- [ ] Test approval workflow
- [ ] Dashboard updating correctly

## Next Steps to Gold Tier

Gold Tier adds:
- Odoo accounting integration
- Facebook/Instagram posting
- Twitter (X) integration
- Weekly CEO briefing
- Ralph Wiggum loop
- Error recovery
- Comprehensive logging

---

**Silver Tier Status: Ready for Production**

You now have a fully autonomous AI Employee with:
- Multi-channel input monitoring
- Automatic task processing
- Human-in-the-loop safety
- Complete audit trail
- Real-time dashboard
