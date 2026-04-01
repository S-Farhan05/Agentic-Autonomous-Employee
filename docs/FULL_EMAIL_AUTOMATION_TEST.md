# Full Email Automation Testing Guide

**Date:** 2026-04-02  
**Status:** Ready for End-to-End Testing

---

## ✅ What's Configured

| Component | Status | Details |
|-----------|--------|---------|
| Gmail OAuth Scopes | ✅ | Read + Send + Compose + Modify |
| Authentication Token | ✅ | Saved with sending permissions |
| Email MCP Server | ✅ | Installed at `mcp-servers/email-mcp/` |
| MCP Dependencies | ✅ | googleapis, @modelcontextprotocol/sdk |
| Qwen Config | ✅ | `qwen-mcp-config.json` created |
| Gmail Watcher | ✅ | Filtering promotional emails |
| Continuous Processor | ✅ | Processes every 5 minutes |

---

## 🧪 Testing Steps

### **Step 1: Start All Services**

Open 2 terminals:

**Terminal 1 - Gmail Watcher:**
```bash
python watchers/gmail_watcher.py
```

**Terminal 2 - Continuous Processor:**
```bash
python scripts/continuous_processor.py
```

---

### **Step 2: Send Test Email**

From another email account (or your phone), send an email to your Gmail:

**To:** Your Gmail address  
**Subject:** `Question: Project Proposal`  
**Body:**
```
Hi,

I wanted to ask about the project proposal we discussed. 
Can you send me the details?

Thanks,
[Your Name]
```

---

### **Step 3: Watch Automation (Wait 2-7 minutes)**

**Timeline:**

| Time | Event | What to Watch |
|------|-------|---------------|
| 0:00 | Email sent | From your phone/another account |
| 0:02 | Watcher detects | Gmail watcher checks every 2 min |
| 0:02 | Task created | `Needs_Action/EMAIL_Question_Project_*.md` |
| 0:05 | Processor runs | Continuous processor invokes Qwen |
| 0:06 | Qwen processes | Reads email, creates approval request |
| 0:06 | Approval created | `Pending_Approval/APPROVAL_Email_Reply_*.md` |

---

### **Step 4: Check for Approval Request**

After 5-7 minutes, check:

```bash
dir AI_Employee_Vault\Pending_Approval
```

You should see:
```
APPROVAL_Email_Reply_[something].md
```

View the approval request:
```bash
type AI_Employee_Vault\Pending_Approval\APPROVAL_Email_Reply_*.md
```

It should contain:
- Email draft reply
- Recipient address
- Subject line
- Professional response
- Instructions to approve/reject

---

### **Step 5: APPROVE the Email (Human-in-the-Loop)**

**To Approve:**
```bash
move AI_Employee_Vault\Pending_Approval\APPROVAL_*.md AI_Employee_Vault\Approved\
```

**To Reject:**
```bash
move AI_Employee_Vault\Pending_Approval\APPROVAL_*.md AI_Employee_Vault\Rejected\
```

**To Edit then Approve:**
```bash
# 1. Edit the file
notepad AI_Employee_Vault\Pending_Approval\APPROVAL_*.md

# 2. Modify the email draft as needed

# 3. Save and move to Approved
move AI_Employee_Vault\Pending_Approval\APPROVAL_*.md AI_Employee_Vault\Approved\
```

---

### **Step 6: Automatic Email Sending**

After you approve (move to `Approved/`):

**Timeline:**

| Time | Event |
|------|-------|
| 0:00 | You move file to Approved/ |
| 0:05 | Next processing cycle detects approval |
| 0:05 | Qwen runs /process-approvals |
| 0:06 | MCP server sends email via Gmail API |
| 0:06 | Email sent! Check your Sent folder |
| 0:07 | Task moved to Done/ |
| 0:07 | Dashboard updated |

---

### **Step 7: Verify Email Was Sent**

**Check Gmail Sent Folder:**
- Open Gmail
- Go to Sent
- Should see your reply email

**Check Logs:**
```bash
type AI_Employee_Vault\Logs\continuous_processor.log
```

Should show:
```
✅ Email sent successfully
✅ Task moved to Done/
```

**Check Dashboard:**
```bash
type AI_Employee_Vault\Dashboard.md
```

Should show:
```
## Recent Activity
- [Timestamp] Email sent to [recipient] - Reply delivered ✅
```

---

## 🎯 Complete Workflow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ 1. EMAIL ARRIVES                                            │
│    From: Someone asking about project                       │
└──────────────────┬──────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. GMAIL WATCHER DETECTS (2 min)                            │
│    ✓ Filters out promotional/PIN emails                     │
│    ✓ Creates task in Needs_Action/                          │
└──────────────────┬──────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. TASK FILE CREATED                                        │
│    Needs_Action/EMAIL_Question_Project_*.md                │
│    - Contains full email content                            │
│    - Priority assigned                                      │
│    - Suggested actions                                      │
└──────────────────┬──────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. CONTINUOUS PROCESSOR (5 min cycle)                       │
│    ✓ Detects new task                                       │
│    ✓ Invokes Qwen Code                                      │
│    ✓ Runs /process-tasks                                    │
└──────────────────┬──────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. QWEN PROCESSES EMAIL                                     │
│    ✓ Reads Company_Handbook.md                              │
│    ✓ Analyzes email content                                 │
│    ✓ Decides: "Reply requires approval"                     │
│    ✓ Creates draft response                                 │
└──────────────────┬──────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────────┐
│ 6. APPROVAL REQUEST CREATED                                 │
│    Pending_Approval/APPROVAL_Email_Reply_*.md              │
│    Contains:                                                │
│    - Draft email to send                                    │
│    - Recipient details                                      │
│    - Context and reasoning                                  │
│    - Instructions: Move to Approved/ or Rejected/           │
└──────────────────┬──────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────────┐
│ 7. HUMAN REVIEWS (YOU!)                                     │
│    Options:                                                 │
│    A) Approve → Move to Approved/                           │
│    B) Reject → Move to Rejected/                            │
│    C) Edit then Approve                                     │
└──────────────────┬──────────────────────────────────────────┘
                   ↓
        ┌────────────────────┐
        ↓                     ↓
┌──────────────┐      ┌──────────────┐
│ APPROVED     │      │ REJECTED     │
└──────┬───────┘      └──────┬───────┘
       ↓                     ↓
┌─────────────────┐   ┌─────────────────┐
│ 8A. AUTO-SEND   │   │ 8B. ARCHIVE     │
│ MCP sends email │   │ Log rejection   │
│ Email sent! ✅  │   │ Move to Done/   │
└──────┬──────────┘   └─────────────────┘
       ↓
┌─────────────────────────────────────────┐
│ 9. COMPLETION                           │
│ ✓ Task moved to Done/                   │
│ ✓ Dashboard updated                     │
│ ✓ Logs show: "Email sent successfully"  │
│ ✓ Gmail Sent folder has the email       │
└─────────────────────────────────────────┘
```

---

## 🔧 Troubleshooting

### **Issue: No approval request created**

**Possible causes:**
- Qwen didn't run yet (wait 5 minutes)
- Task still in Needs_Action/
- Continuous processor not running

**Fix:**
```bash
# Check if processor is running
tasklist | findstr python

# If not running, restart:
python scripts/continuous_processor.py
```

---

### **Issue: Email not sending after approval**

**Check:**
1. MCP server configured correctly
2. Token has sending scopes
3. Check logs for errors

**Fix:**
```bash
# Check logs
type AI_Employee_Vault\Logs\continuous_processor.log

# Verify token exists
dir credentials\token.pickle

# If token old, re-authenticate:
del credentials\token.pickle
python scripts/test_gmail_auth.py
```

---

### **Issue: MCP server not found**

**Fix:**
```bash
# Verify installation
cd mcp-servers\email-mcp
dir

# Should see: index.js, package.json, node_modules/

# Test MCP server manually:
node index.js
# Should say: "Email MCP Server running on stdio"
```

---

### **Issue: Permission denied when sending**

**Cause:** Gmail API permissions not granted

**Fix:**
```bash
# Re-authenticate with full permissions
del credentials\token.pickle
python scripts/test_gmail_auth.py
# Make sure to allow ALL requested permissions
```

---

## ✅ Success Criteria

Full email automation is working when:

- [ ] Email arrives → Task created within 2 min
- [ ] Qwen processes → Approval created within 5 min
- [ ] You approve → Email sends within 5 min
- [ ] Email appears in Gmail Sent folder
- [ ] Dashboard shows "Email sent successfully"
- [ ] Task moved to Done/ folder
- [ ] Logs show successful execution

---

## 🎯 Test Scenarios

### **Scenario 1: Simple Reply (Tested Above)**
- Email asking question → Approve reply → Sent ✅

### **Scenario 2: Edit Before Sending**
```bash
# 1. Approval request created
# 2. You edit the draft in Pending_Approval/
# 3. Move to Approved/
# 4. Your edited version sends
```

### **Scenario 3: Reject Email**
```bash
# 1. Approval request created
# 2. You move to Rejected/
# 3. Task archived, no email sent
```

### **Scenario 4: High Priority Email**
```bash
# Send email with subject: "URGENT: Meeting Today"
# Should get priority: high
# Faster processing (next cycle)
```

---

## 📊 Expected Timing

| Phase | Duration | Total Time |
|-------|----------|------------|
| Email detection | 0-2 min | 2 min |
| Task creation | < 10 sec | 2 min |
| Qwen processing | 0-5 min | 7 min |
| Approval creation | < 30 sec | 7 min |
| **Human review** | **You control** | **Varies** |
| Auto-execution | 0-5 min | 12 min + review time |

**Total (excluding human review): ~12 minutes**

---

## 🚀 Ready to Test?

**Commands to start:**

```bash
# Terminal 1
python watchers/gmail_watcher.py

# Terminal 2
python scripts/continuous_processor.py

# Then send test email and watch the magic! ✨
```

---

**Let me know when you're ready to start the test!**
