# Silver Tier - Complete User Guide

**Personal AI Employee - Autonomous Email & Social Media Automation**

This guide covers everything you need to run the Silver Tier AI Employee system.

---

## 📋 Table of Contents

1. [What is Silver Tier?](#what-is-silver-tier)
2. [System Architecture](#system-architecture)
3. [Quick Start - Run Everything](#quick-start---run-everything)
4. [Gmail Automation](#gmail-automation)
5. [LinkedIn Auto-Posting](#linkedin-auto-posting)
6. [File Drop Automation](#file-drop-automation)
7. [Approval Workflow](#approval-workflow)
8. [Monitoring & Logs](#monitoring--logs)
9. [Troubleshooting](#troubleshooting)
10. [Configuration](#configuration)

---

## What is Silver Tier?

Silver Tier is an autonomous AI employee that:

| Feature | Description |
|---------|-------------|
| 📧 **Gmail Automation** | Monitors inbox, creates tasks, drafts replies, sends with approval |
| 💼 **LinkedIn Posting** | Auto-generates and publishes professional posts |
| 📁 **File Drop** | Monitors folder for files, processes automatically |
| 🤖 **Continuous Processing** | Runs every 2 minutes, no manual intervention needed |
| ✅ **Human-in-the-Loop** | All external actions require your approval first |

### **Tier Progress**

```
🥉 Bronze   ✅ Complete - Foundation, file watcher
🥈 Silver   ✅ Complete - Gmail + LinkedIn automation
🥇 Gold     ⏳ Pending - Odoo ERP, WhatsApp, weekly audits
💎 Platinum ⏳ Pending - Cloud deployment, 24/7 operation
```

---

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  INPUT SOURCES                          │
│    Gmail Emails    │    LinkedIn    │   File Drops     │
└─────────┬──────────┴────────┬───────┴────────┬─────────┘
          │                   │                │
          ▼                   ▼                ▼
┌─────────────────────────────────────────────────────────┐
│                  WATCHERS (Senses)                      │
│  gmail_watcher.py   │  linkedin_poster.py  │  filesystem│
│  (every 2 min)      │  (on demand)         │  (on event)│
└─────────┬───────────┴──────────────────────┴────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────┐
│               AI_EMPLOYEE_VAULT (Memory)                │
│  /Needs_Action/ → /Pending_Approval/ → /Approved/      │
│  /Done/ │ /Plans/ │ /Logs/ │ Dashboard.md              │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│           CONTINUOUS PROCESSOR (Heartbeat)              │
│  Runs every 2 minutes → Invokes Qwen Code               │
│  Reads tasks → Creates approvals → Updates dashboard    │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                  ACTION LAYER                           │
│  send_approved_email.py  │  linkedin_poster.py         │
│  (Gmail API)             │  (Playwright browser)        │
└─────────────────────────────────────────────────────────┘
```

---

## Quick Start - Run Everything

### **Prerequisites Check**

```bash
# 1. Navigate to project
cd E:\Farhan-work\Hackathon\Agentic-Autonomous-Employee

# 2. Install dependencies (first time only)
pip install -r requirements.txt

# 3. Verify Qwen Code is installed
qwen --version

# 4. Verify folder structure
dir AI_Employee_Vault
```

### **Start All Automation (3 Terminals)**

**Terminal 1 - Gmail Watcher:**
```bash
cd E:\Farhan-work\Hackathon\Agentic-Autonomous-Employee
python watchers/gmail_watcher.py
```

**Terminal 2 - Continuous Processor:**
```bash
cd E:\Farhan-work\Hackathon\Agentic-Autonomous-Employee
python scripts/continuous_processor.py
```

**Terminal 3 - Monitor Progress:**
```bash
cd E:\Farhan-work\Hackathon\Agentic-Autonomous-Employee
# Watch folders
dir AI_Employee_Vault\Needs_Action\*.md
dir AI_Employee_Vault\Pending_Approval\*.md
dir AI_Employee_Vault\Approved\*.md
```

### **Test the System**

1. **Send an email** to your Gmail address with subject: `Test: Hello`
2. **Wait 2 minutes** - Gmail Watcher detects it
3. **Wait 2 more minutes** - Continuous Processor invokes Qwen
4. **Check `Pending_Approval/`** - Approval request created
5. **Move file to `Approved/`** - You approve
6. **Wait 2 minutes** - Email reply sent automatically
7. **Check `Done/`** - Task completed!

---

## Gmail Automation

### **What It Does**

1. Monitors your Gmail inbox every 2 minutes
2. Filters out promotional/security emails automatically
3. Creates task files for important emails
4. Qwen drafts professional responses
5. You approve via file move
6. Email sent via Gmail API

### **Setup (First Time Only)**

**1. Gmail API Credentials:**
```bash
# Ensure credentials exist
dir credentials\credentials.json
```

If missing:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create project → Enable Gmail API
3. Create OAuth 2.0 credentials
4. Download as `credentials.json`
5. Place in `credentials/` folder

**2. OAuth Authentication:**
```bash
# First run will open browser for authentication
python watchers/gmail_watcher.py
# → Browser opens → Log in → Allow permissions → Token saved
```

### **Email Filtering**

Automatically **IGNORES**:
- Promotional emails (Netflix, Amazon, etc.)
- Security/PIN emails
- Newsletters
- No-reply senders

**Customize filters** in `watchers/gmail_watcher.py`:
```python
ignore_senders = ['noreply', 'linkedin', 'amazon', 'netflix']
ignore_subjects = ['PIN', 'verification', 'promo', 'newsletter']
```

### **Email Workflow**

```
Email arrives → Gmail (2 min)
    ↓
gmail_watcher.py detects
    ↓
Creates: Needs_Action/EMAIL_Subject_*.md
    ↓
continuous_processor.py (2 min) → Qwen Code
    ↓
Creates: Pending_Approval/EMAIL_APPROVAL_*.md
    ↓
YOU: Move file to Approved/
    ↓
Next cycle → send_approved_email.py
    ↓
Email sent via Gmail API → Done/
```

### **Commands**

```bash
# Start Gmail Watcher
python watchers/gmail_watcher.py

# View Gmail logs
type AI_Employee_Vault\Logs\gmail_watcher.log

# Check email tasks
dir AI_Employee_Vault\Needs_Action\EMAIL_*.md

# Check pending approvals
dir AI_Employee_Vault\Pending_Approval\EMAIL_*.md

# View email action log
type AI_Employee_Vault\Logs\email_actions.json
```

---

## LinkedIn Auto-Posting

### **What It Does**

1. Opens browser and navigates to LinkedIn
2. Clicks "Start a post"
3. Types your content
4. Clicks "Post"
5. Logs the action
6. Takes debug screenshots

### **Create Post Content**

**Method 1: Text File (Recommended)**

Create `linkedin_post_content.txt`:
```
Just Completed Silver Tier: AI Employee Automation System

I'm excited to share my latest project - a local-first Personal AI Employee 
that automates daily business tasks autonomously!

What It Does:
- Gmail Automation: Detects emails, drafts responses, sends with approval
- LinkedIn Auto-Posting: Generates and publishes professional content  
- 24/7 Monitoring: Continuous processing every 2 minutes

Tech Stack:
- Qwen Code as the reasoning engine
- Python + Playwright for automation
- Gmail API for email sending

#AIAgent #Automation #Productivity #AI #MachineLearning
```

**Method 2: Command Line**
```bash
python scripts/linkedin_poster.py "Your post content here"
```

### **Post to LinkedIn**

```bash
# From file (recommended for long posts)
python scripts/linkedin_poster.py linkedin_post_content.txt

# Direct content (short posts only)
python scripts/linkedin_poster.py "Quick update about my project"
```

### **What Happens**

```
1. Browser launches (visible)
2. Navigates to LinkedIn login
3. You log in manually (first time)
4. Script detects successful login
5. Clicks "Start a post" button
6. Types content from file
7. Clicks "Post" button
8. Waits for confirmation
9. Saves debug screenshots
10. Logs action to Logs/linkedin_posts.log
```

### **Debug Screenshots**

Screenshots saved to `debug/` folder:
- `linkedin_debug.png` - After page load
- `linkedin_modal_debug.png` - After clicking "Start a post"

**Note:** `debug/` folder is in `.gitignore` - not pushed to GitHub

### **Troubleshooting LinkedIn**

**Issue: Can't find editor**
- Solution: Script uses fallback keyboard input - works reliably

**Issue: Login timeout**
- Solution: Keep browser window visible, complete 2FA if prompted

**Issue: Post button not found**
- Solution: Script tries 10+ selectors - check debug screenshots

---

## File Drop Automation

### **What It Does**

Monitors `AI_Employee_Vault/Inbox/` folder for new files and creates tasks automatically.

### **Usage**

```bash
# 1. Start File Watcher
python watchers/filesystem_watcher.py

# 2. Drop a file
echo "Process this document" > AI_Employee_Vault\Inbox\document.txt

# 3. Watcher creates task
# Needs_Action/FILE_document.txt.md
```

### **Workflow**

```
File dropped → Inbox/
    ↓
filesystem_watcher.py detects
    ↓
Creates: Needs_Action/FILE_*.md
    ↓
continuous_processor.py → Qwen Code
    ↓
Processes file → Done/
```

---

## Approval Workflow

### **How It Works**

All external actions (emails, posts) require your approval before execution.

### **Approval Process**

**Step 1: Qwen Creates Approval Request**
```
Pending_Approval/EMAIL_APPROVAL_Greeting.md
---
type: approval_request
action: send_email
to: sfarhaniqbal2005@gmail.com
subject: Re: Greeting
---

## Email Draft
Dear Sender,
Thank you for reaching out...

## To Approve
Move this file to /Approved folder
```

**Step 2: You Review**
```bash
# Read the draft
type AI_Employee_Vault\Pending_Approval\EMAIL_APPROVAL_Greeting.md
```

**Step 3: You Approve (Choose One)**

**Approve:**
```bash
move AI_Employee_Vault\Pending_Approval\*.md AI_Employee_Vault\Approved\
```

**Reject:**
```bash
move AI_Employee_Vault\Pending_Approval\*.md AI_Employee_Vault\Rejected\
```

**Step 4: Next Cycle Executes**
```
continuous_processor.py (2 min) → Qwen Code
    ↓
Detects file in Approved/
    ↓
send_approved_email.py executes
    ↓
Email sent → Moved to Done/
```

### **Approval Rules**

| Action | Requires Approval? |
|--------|-------------------|
| Reading emails | ❌ No (auto-approved) |
| Drafting responses | ❌ No (auto-approved) |
| Sending emails | ✅ Yes |
| LinkedIn posts | ✅ Yes |
| File operations | ❌ No (auto-approved) |
| Payments | ✅ Yes (Gold tier) |

---

## Monitoring & Logs

### **Dashboard**

```bash
# View current status
type AI_Employee_Vault\Dashboard.md
```

Shows:
- Recent activity
- Pending tasks count
- Awaiting approvals count
- Completed tasks this week

### **Logs**

```bash
# Gmail Watcher logs
type AI_Employee_Vault\Logs\gmail_watcher.log

# Continuous Processor logs
type AI_Employee_Vault\Logs\continuous_processor.log

# Email actions (JSON)
type AI_Employee_Vault\Logs\email_actions.json

# LinkedIn posts (JSON)
type AI_Employee_Vault\Logs\linkedin_posts.log

# File watcher logs
type AI_Employee_Vault\Logs\filesystem_watcher.log
```

### **Folder Status**

```bash
# Tasks waiting for processing
dir AI_Employee_Vault\Needs_Action\*.md

# Awaiting your approval
dir AI_Employee_Vault\Pending_Approval\*.md

# Ready to execute
dir AI_Employee_Vault\Approved\*.md

# Completed today
dir AI_Employee_Vault\Done\*.md
```

---

## Troubleshooting

### **Gmail Watcher Issues**

**Error: `ModuleNotFoundError: No module named 'google'`**
```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

**Error: `credentials.json not found`**
```bash
# Download from Google Cloud Console
# Place in credentials/ folder
dir credentials\credentials.json
```

**Error: `Token expired`**
```bash
# Delete old token
del credentials\token.pickle
# Re-run watcher to re-authenticate
python watchers/gmail_watcher.py
```

**Emails not being detected**
```bash
# Check logs
type AI_Employee_Vault\Logs\gmail_watcher.log

# Verify watcher is running
# Check for "GMAIL WATCHER STARTED" in logs

# Test manually
python watchers/gmail_watcher.py
```

### **Continuous Processor Issues**

**Error: `qwen: command not found`**
```bash
# Install Qwen Code
npm install -g @anthropic/claude-code
```

**Qwen not creating approvals**
```bash
# Test manually
qwen -y "Read AI_Employee_Vault/Needs_Action/*.md and create approval requests"

# Check Company Handbook exists
type AI_Employee_Vault\Company_Handbook.md
```

**Processing too slow**
```bash
# Reduce interval (default: 120 seconds)
python scripts/continuous_processor.py AI_Employee_Vault 60
```

### **LinkedIn Poster Issues**

**Error: `ModuleNotFoundError: No module named 'playwright'`**
```bash
pip install playwright
playwright install chromium
```

**Browser won't launch**
```bash
# Reinstall Playwright browsers
playwright install chromium --force
```

**Can't find Post button**
```bash
# Check debug screenshots
dir debug\*.png

# LinkedIn may have updated UI
# Check logs for which selectors failed
type AI_Employee_Vault\Logs\linkedin_posts.log
```

### **General Issues**

**Files not moving between folders**
```bash
# Check file permissions
# Ensure no other process has files open

# Manual move if needed
move AI_Employee_Vault\Needs_Action\*.md AI_Employee_Vault\Done\
```

**Dashboard not updating**
```bash
# Check if file is locked
# Restart continuous processor
# Manual update - edit Dashboard.md directly
```

---

## Configuration

### **Processing Interval**

Default: **120 seconds (2 minutes)**

```bash
# Custom interval
python scripts/continuous_processor.py AI_Employee_Vault 300
# Now runs every 5 minutes
```

### **Gmail Check Interval**

Default: **120 seconds (2 minutes)**

```bash
# Custom interval
python watchers/gmail_watcher.py AI_Employee_Vault 300
# Now checks every 5 minutes
```

### **Email Filters**

Edit `watchers/gmail_watcher.py`:
```python
# Add more senders to ignore
ignore_senders = [
    'noreply', 'no-reply', 'security-noreply',
    'linkedin', 'facebook', 'twitter',
    'amazon', 'netflix', 'spotify',
    'your-custom-sender@example.com'  # Add here
]
```

### **Company Rules**

Edit `AI_Employee_Vault/Company_Handbook.md`:
```markdown
## Add Custom Rules

### Payment Threshold
- Flag transactions over $500 for review

### Response Time
- Reply to VIP clients within 1 hour

### Working Hours
- Active: 9 AM - 6 PM local time
```

### **Qwen Skills**

Located in `.qwen/skills/`:
- `process-tasks.md` - Task processing logic
- `process-approvals.md` - Approval workflow
- `send-email.md` - Email drafting & sending
- `post-linkedin.md` - LinkedIn content creation
- `create-plan.md` - Multi-step task planning
- `continuous-processing.md` - 24/7 automation guide

---

## Daily Operations Checklist

### **Morning (Start Automation)**

```bash
# Terminal 1
python watchers/gmail_watcher.py

# Terminal 2  
python scripts/continuous_processor.py

# Check status
type AI_Employee_Vault\Dashboard.md
```

### **During Day (Monitor)**

```bash
# Check for approvals needed
dir AI_Employee_Vault\Pending_Approval\*.md

# Review and approve
type AI_Employee_Vault\Pending_Approval\*.md
move AI_Employee_Vault\Pending_Approval\*.md AI_Employee_Vault\Approved\
```

### **Evening (Review)**

```bash
# Check what was completed
dir AI_Employee_Vault\Done\*.md

# Review logs
type AI_Employee_Vault\Logs\email_actions.json
type AI_Employee_Vault\Logs\linkedin_posts.log

# Stop watchers (Ctrl+C in each terminal)
```

### **Weekly Maintenance**

```bash
# Archive old logs
# Review Company Handbook
# Update Dashboard stats
# Check for pending items
```

---

## Quick Reference Commands

```bash
# START EVERYTHING
python watchers/gmail_watcher.py
python scripts/continuous_processor.py

# CHECK STATUS
type AI_Employee_Vault\Dashboard.md
dir AI_Employee_Vault\Needs_Action\*.md
dir AI_Employee_Vault\Pending_Approval\*.md

# APPROVE ACTIONS
type AI_Employee_Vault\Pending_Approval\*.md
move AI_Employee_Vault\Pending_Approval\*.md AI_Employee_Vault\Approved\

# POST TO LINKEDIN
python scripts/linkedin_poster.py linkedin_post_content.txt

# VIEW LOGS
type AI_Employee_Vault\Logs\gmail_watcher.log
type AI_Employee_Vault\Logs\continuous_processor.log

# TEST GMAIL
python watchers/gmail_watcher.py
```

---

## What's Next? (Gold Tier)

After mastering Silver Tier, upgrade to Gold:

- [ ] **Odoo ERP Integration** - Accounting automation
- [ ] **WhatsApp Watcher** - Message monitoring
- [ ] **Weekly CEO Briefing** - Auto-generated reports
- [ ] **Payment Processing** - With approval workflow
- [ ] **Multi-domain Automation** - Email + Social + Finance

---

**Silver Tier Status: ✅ Complete**

**Built with Qwen Code | Local-First AI Employee**

For questions or issues, check the `docs/` folder for detailed guides.
