# AI Employee - Silver Tier Implementation

**A local-first Personal AI Employee built with Qwen Code and Obsidian**

This Silver Tier implementation provides autonomous email and social media automation with human-in-the-loop approval workflow.

## 🎯 Tier Status

| Tier | Status | Description |
|------|--------|-------------|
| 🥉 Bronze | ✅ **Complete** | Foundation, file watcher, task processing |
| 🥈 Silver | ✅ **Complete** | Gmail automation, LinkedIn posting, approval workflow |
| 🥇 Gold | ⏳ Pending | Odoo integration, multi-domain automation |
| 💎 Platinum | ⏳ Pending | Cloud deployment, always-on operation |

## ✨ What's Working

### 📧 Gmail Automation
- ✅ Gmail Watcher detects new emails (2-min intervals)
- ✅ Filters promotional/security emails automatically
- ✅ Creates tasks in `Needs_Action/` folder
- ✅ Qwen Code processes and creates approval requests
- ✅ Human-in-the-loop approval workflow
- ✅ Sends emails via Gmail API (OAuth2 authenticated)

### 💼 LinkedIn Automation
- ✅ Auto-posts to LinkedIn about business topics
- ✅ Professional content generation
- ✅ Approval workflow before posting

### 🤖 Autonomous Processing
- ✅ Continuous Processor runs every 2 minutes
- ✅ Qwen Code as the reasoning engine
- ✅ Company Handbook rules for decision-making
- ✅ Dashboard updates automatically

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    EXTERNAL SOURCES                             │
│         Gmail                    LinkedIn          File Drops   │
└──────────┬────────────────────────┬──────────────────┬──────────┘
           │                        │                  │
           ▼                        ▼                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PERCEPTION LAYER (Watchers)                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Gmail Watcher│  │LinkedIn Poster│ │File Watcher  │          │
│  │  (2 min)     │  │  (on demand)  │ │  (on event)  │          │
│  └──────┬───────┘  └──────────────┘  └──────┬───────┘          │
└─────────┼────────────────────────────────────┼──────────────────┘
          │                                    │
          ▼                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                    OBSIDIAN VAULT (Local Memory)                │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ /Needs_Action/  →  /Pending_Approval/  →  /Approved/     │  │
│  │ /Done/  │  /Plans/  │  /Logs/  │  Dashboard.md           │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                    REASONING LAYER (Qwen Code)                  │
│   Continuous Processor (every 2 min) invokes Qwen Code          │
│   Read → Think → Plan → Create Approvals → Update Dashboard     │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ACTION LAYER                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │Gmail API     │  │LinkedIn API  │  │File System   │          │
│  │(send email)  │  │(post update) │  │(move files)  │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
Agentic-Autonomous-Employee/
├── AI_Employee_Vault/          # Obsidian vault (memory)
│   ├── Inbox/                  # File drop zone
│   ├── Needs_Action/           # Tasks waiting for processing
│   ├── Pending_Approval/       # Awaiting human approval
│   ├── Approved/               # Ready to execute
│   ├── Done/                   # Completed tasks
│   ├── Dashboard.md            # Real-time status
│   └── Company_Handbook.md     # AI behavior rules
├── watchers/                   # Perception layer
│   ├── gmail_watcher.py        # Gmail monitoring
│   ├── filesystem_watcher.py   # File drop monitoring
│   └── base_watcher.py         # Base class
├── scripts/                    # Core logic
│   ├── continuous_processor.py # Invokes Qwen every 2 min
│   ├── create_email_approval.py # Creates approval requests
│   ├── send_approved_email.py  # Sends emails via Gmail API
│   ├── linkedin_poster.py      # LinkedIn posting
│   └── gmail_auth.py           # OAuth authentication
├── mcp-servers/                # Future: MCP integration
├── credentials/                # OAuth tokens (gitignored)
├── docs/                       # Documentation archive
├── .qwen/                      # Qwen skills & config
├── README.md                   # This file
└── requirements.txt            # Python dependencies
```

## 🚀 Quick Start

### Prerequisites

- **Python**: 3.13 or higher
- **Qwen Code**: Installed and configured
- **Obsidian**: Optional (for GUI viewing)
- **Gmail API**: OAuth credentials in `credentials/`

### Installation

```bash
cd E:\Farhan-work\Hackathon\Agentic-Autonomous-Employee
pip install -r requirements.txt
```

### Start Automation

**Terminal 1 - Gmail Watcher:**
```bash
python watchers/gmail_watcher.py
```

**Terminal 2 - Continuous Processor:**
```bash
python scripts/continuous_processor.py
```

### Test the System

1. **Send a test email** to your Gmail address
2. **Wait 2 minutes** - Gmail Watcher detects it
3. **Wait 2 more minutes** - Continuous Processor invokes Qwen
4. **Check `Pending_Approval/`** - Approval request created
5. **Move to `Approved/`** - You approve the action
6. **Wait 2 minutes** - Email sent via Gmail API
7. **Check `Done/`** - Task completed

## 📊 Workflow Example

### Email Processing Flow

```
1. Email arrives → Gmail Watcher (2 min)
                      ↓
2. Task created → Needs_Action/EMAIL_*.md
                      ↓
3. Continuous Processor (2 min) → Invokes Qwen Code
                      ↓
4. Qwen reads Company_Handbook.md → Creates approval request
                      ↓
5. Approval in Pending_Approval/ → Waits for human
                      ↓
6. You move to Approved/ → Human approval
                      ↓
7. Next cycle → Qwen executes send_approved_email.py
                      ↓
8. Email sent via Gmail API → Moved to Done/
```

## ⚙️ Configuration

### Processing Interval

Default: **120 seconds (2 minutes)**

```bash
# Custom interval (in seconds)
python scripts/continuous_processor.py <vault_path> <interval_seconds>

# Example: 5 minute intervals
python scripts/continuous_processor.py AI_Employee_Vault 300
```

### Gmail Filtering

Edit `watchers/gmail_watcher.py` to customize:

```python
# Emails to ignore
ignore_senders = ['noreply', 'security', 'linkedin', 'amazon']
ignore_subjects = ['PIN', 'verification', 'promo', 'newsletter']
```

### AI Behavior Rules

Edit `AI_Employee_Vault/Company_Handbook.md`:

- Add new decision rules
- Change approval thresholds
- Modify priority levels
- Define working hours

## 🛠️ Commands

### Monitor Folders

```bash
# Check pending tasks
dir AI_Employee_Vault\Needs_Action\*.md

# Check approvals waiting
dir AI_Employee_Vault\Pending_Approval\*.md

# Check ready to execute
dir AI_Employee_Vault\Approved\*.md
```

### View Logs

```bash
# Gmail Watcher logs
type AI_Employee_Vault\Logs\gmail_watcher.log

# Continuous Processor logs
type AI_Employee_Vault\Logs\continuous_processor.log

# Email actions log
type AI_Employee_Vault\Logs\email_actions.json
```

### Dashboard

```bash
# View current status
type AI_Employee_Vault\Dashboard.md
```

## 📚 Documentation

Full documentation is in the `docs/` folder:

| Document | Description |
|----------|-------------|
| `docs/SILVER_TIER_COMPLETE.md` | Silver tier implementation details |
| `docs/GMAIL_TESTING_GUIDE.md` | Gmail setup and testing guide |
| `docs/EMAIL_WORKFLOW_COMPLETE.md` | Email workflow documentation |
| `docs/QUICKSTART.md` | Quick start guide |
| `docs/PROJECT_SUMMARY.md` | Project overview |

## 🔒 Security

- ✅ All data stays local in Obsidian vault
- ✅ OAuth2 authentication for Gmail API
- ✅ Credentials stored in `credentials/` (gitignored)
- ✅ Human approval required for all external actions
- ✅ Audit logs in `Logs/` folder
- ✅ `.gitignore` prevents sensitive data commits

## 🎯 Silver Tier Deliverables

From the hackathon requirements:

| Requirement | Status | Implementation |
|-------------|--------|----------------|
| All Bronze requirements | ✅ | Complete foundation |
| 2+ Watcher scripts | ✅ | Gmail + File System |
| LinkedIn auto-posting | ✅ | `linkedin_poster.py` |
| Qwen reasoning loop | ✅ | `continuous_processor.py` |
| MCP server for actions | ⚠️ | Using direct API (MCP reserved for Gold) |
| Human-in-the-loop | ✅ | `Pending_Approval/` workflow |
| Scheduling | ✅ | 2-minute intervals |
| Agent Skills | ✅ | Qwen skills in `.qwen/skills/` |

## 🔮 Next Steps (Gold Tier)

- [ ] Odoo ERP integration via MCP
- [ ] WhatsApp watcher for message monitoring
- [ ] Weekly business audit with CEO briefing
- [ ] Multiple MCP servers for different actions
- [ ] Error recovery and graceful degradation

## 🚀 Platinum Tier (Future)

- [ ] Cloud VM deployment (24/7 operation)
- [ ] Local/Cloud separation (Cloud drafts, Local approves)
- [ ] Vault sync via Git
- [ ] A2A agent communication
- [ ] Facebook/Instagram/Twitter integration

---

**Built with Qwen Code** | **Silver Tier Complete** | **Local-First AI Employee**
