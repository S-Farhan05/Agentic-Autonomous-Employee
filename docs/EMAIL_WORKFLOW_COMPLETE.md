# Complete Email Workflow: Detection → Approval → Sending

**Date:** 2026-04-01  
**Status:** Full automation with Continuous Processor

---

## Visual Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                    STEP 1: EMAIL ARRIVES                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  📧 Gmail Inbox                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ From: client@company.com                                     │   │
│  │ Subject: Urgent: Need invoice for March services            │   │
│  │ Date: Apr 1, 2026, 10:00 AM                                 │   │
│  │                                                              │   │
│  │ Hi,                                                          │   │
│  │                                                              │   │
│  │ Could you please send me the invoice for March?             │   │
│  │ We need it for accounting.                                   │   │
│  │                                                              │   │
│  │ Thanks,                                                      │   │
│  │ John                                                         │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  Action: Gmail Watcher checks every 2 minutes                      │
└─────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│              STEP 2: GMAIL WATCHER DETECTS                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ⏰ Time: 10:01 AM (1 minute later)                                │
│                                                                     │
│  Gmail Watcher:                                                     │
│  ✓ Checks Gmail API                                                 │
│  ✓ Query: is:unread (is:important OR subject:invoice)              │
│  ✓ Finds: 1 new email                                              │
│  ✓ Extracts: sender, subject, body, priority                       │
│  ✓ Detects keyword: "invoice" → HIGH PRIORITY                      │
│                                                                     │
│  Action: Creates task file in Needs_Action/                        │
└─────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│              STEP 3: TASK CREATED IN NEEDS_ACTION                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  📁 Folder: AI_Employee_Vault/Needs_Action/                        │
│                                                                     │
│  📄 File Created:                                                   │
│  EMAIL_Urgent_Need_Invoice_abc123.md                               │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ ---                                                          │   │
│  │ type: email                                                  │   │
│  │ from: client@company.com                                     │   │
│  │ subject: Urgent: Need invoice for March services            │   │
│  │ received: 2026-04-01T10:01:00                               │   │
│  │ priority: high                                               │   │
│  │ status: pending                                              │   │
│  │ gmail_id: abc123                                             │   │
│  │ ---                                                          │   │
│  │                                                              │   │
│  │ ## Email from client@company.com                            │   │
│  │                                                              │   │
│  │ **Subject:** Urgent: Need invoice for March services        │   │
│  │ **Priority:** high                                           │   │
│  │                                                              │   │
│  │ ## Email Content                                             │   │
│  │                                                              │   │
│  │ Hi,                                                          │   │
│  │ Could you please send me the invoice for March?             │   │
│  │                                                              │   │
│  │ ## Suggested Actions                                         │   │
│  │ - [ ] Read full email                                        │   │
│  │ - [ ] Draft response                                         │   │
│  │ - [ ] Create approval request if reply needed                │   │
│  │ - [ ] Move to Done when processed                            │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  Action: Continuous Processor will detect in next cycle           │
└─────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│         STEP 4: CONTINUOUS PROCESSOR DETECTS TASK                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ⏰ Time: 10:05 AM (4 minutes later - next 5-min cycle)           │
│                                                                     │
│  Continuous Processor:                                              │
│  ✓ Runs every 5 minutes                                            │
│  ✓ Checks Needs_Action/ folder                                     │
│  ✓ Finds: 1 task                                                   │
│  ✓ Checks Approved/ folder                                         │
│  ✓ Finds: 0 approvals                                              │
│                                                                     │
│  📝 Log Entry:                                                      │
│  "Found 1 task(s) + 0 approval(s) to process"                      │
│                                                                     │
│  Action: Invokes Qwen Code                                         │
└─────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│              STEP 5: QWEN PROCESSES THE TASK                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ⏰ Time: 10:05 AM                                                  │
│                                                                     │
│  Qwen Code executes:                                                │
│  1. /process-approvals (nothing to approve yet)                    │
│  2. /process-tasks                                                  │
│                                                                     │
│  Qwen reads:                                                        │
│  ✓ Company_Handbook.md → Rules for email handling                  │
│  ✓ EMAIL_Urgent_Need_Invoice_abc123.md → Task content              │
│  ✓ Business_Goals.md → Client communication guidelines             │
│                                                                     │
│  Company_Handbook.md says:                                          │
│  "Email responses require human approval before sending"           │
│                                                                     │
│  Qwen decides:                                                      │
│  "I need to draft a reply and create an approval request"          │
│                                                                     │
│  Action: Creates draft email + approval request                    │
└─────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│         STEP 6: APPROVAL REQUEST CREATED                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  📁 Folder: AI_Employee_Vault/Pending_Approval/                    │
│                                                                     │
│  📄 File Created:                                                   │
│  APPROVAL_Email_Reply_client_abc123.md                             │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ ---                                                          │   │
│  │ type: approval_request                                       │   │
│  │ action: send_email                                           │   │
│  │ to: client@company.com                                       │   │
│  │ subject: Re: Urgent: Need invoice for March services        │   │
│  │ priority: high                                               │   │
│  │ created: 2026-04-01T10:05:00                                │   │
│  │ expires: 2026-04-02T10:05:00                                │   │
│  │ ---                                                          │   │
│  │                                                              │   │
│  │ ## Email Draft                                               │   │
│  │                                                              │   │
│  │ **To:** client@company.com                                   │   │
│  │ **Subject:** Re: Urgent: Need invoice for March services    │   │
│  │                                                              │   │
│  │ ---                                                          │   │
│  │                                                              │   │
│  │ Dear John,                                                   │   │
│  │                                                              │   │
│  │ Thank you for reaching out.                                  │   │
│  │                                                              │   │
│  │ Please find attached the invoice for March services.        │   │
│  │ The total amount is $X,XXX.00, due within 30 days.          │   │
│  │                                                              │   │
│  │ If you have any questions, please let me know.              │   │
│  │                                                              │   │
│  │ Best regards,                                                │   │
│  │ [Your Name]                                                  │   │
│  │                                                              │   │
│  │ ---                                                          │   │
│  │                                                              │   │
│  │ ## Context                                                   │   │
│  │ Client requesting invoice for March services.               │   │
│  │                                                              │   │
│  │ ## To Approve                                                │   │
│  │ Move this file to /Approved folder                          │   │
│  │                                                              │   │
│  │ ## To Reject                                                 │   │
│  │ Move this file to /Rejected folder                          │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  Action: Dashboard updates, waits for human approval              │
└─────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│              STEP 7: DASHBOARD UPDATES                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  📁 File: AI_Employee_Vault/Dashboard.md                           │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ # AI Employee Dashboard                                     │   │
│  │                                                              │   │
│  │ ## System Status                                            │   │
│  │ - Status: Active                                            │   │
│  │ - Last Check: 2026-04-01 10:05                             │   │
│  │ - Pending Tasks: 1                                          │   │
│  │ - Completed Today: 0                                        │   │
│  │                                                              │   │
│  │ ## Recent Activity                                          │   │
│  │ - [2026-04-01 10:05] Email task created:                    │   │
│  │   client@company.com - Invoice request                      │   │
│  │ - [2026-04-01 10:05] Approval request created               │   │
│  │                                                              │   │
│  │ ## Pending Actions                                          │   │
│  │ ⚠️ 1 approval waiting in Pending_Approval/                  │   │
│  │                                                              │   │
│  │ ## Quick Stats                                              │   │
│  │ - Tasks in Queue: 1                                         │   │
│  │ - Awaiting Approval: 1                                      │   │
│  │ - Completed This Week: 0                                    │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  Action: YOU see notification and review approval                 │
└─────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│        STEP 8: HUMAN REVIEWS AND APPROVES (YOU DO THIS)             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ⏰ Time: 10:10 AM (5 minutes later)                               │
│                                                                     │
│  You see Dashboard notification: "1 approval waiting"              │
│                                                                     │
│  You open: Pending_Approval/APPROVAL_Email_Reply_client_abc123.md │
│                                                                     │
│  You review the draft email:                                       │
│  ✓ Recipient correct? ✓                                            │
│  ✓ Subject correct? ✓                                              │
│  ✓ Content appropriate? ✓                                          │
│  ✓ Tone professional? ✓                                            │
│                                                                     │
│  You approve:                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ move Pending_Approval\APPROVAL_Email_Reply_client_abc123.md │   │
│  │      Approved\                                               │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  Action: File moved to Approved/ folder                           │
└─────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│              STEP 9: APPROVAL IN APPROVED/ FOLDER                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  📁 Folder: AI_Employee_Vault/Approved/                            │
│                                                                     │
│  📄 File Present:                                                   │
│  APPROVAL_Email_Reply_client_abc123.md                             │
│                                                                     │
│  Status: Ready for automatic execution                             │
│                                                                     │
│  Action: Continuous Processor will detect in next cycle           │
└─────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│       STEP 10: CONTINUOUS PROCESSOR DETECTS APPROVAL                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ⏰ Time: 10:15 AM (5 minutes later - next cycle)                 │
│                                                                     │
│  Continuous Processor:                                              │
│  ✓ Runs (every 5 minutes)                                          │
│  ✓ Checks Needs_Action/ folder                                     │
│  ✓ Finds: 0 tasks                                                  │
│  ✓ Checks Approved/ folder ← KEY DIFFERENCE FROM ORCHESTRATOR!    │
│  ✓ Finds: 1 approval                                               │
│                                                                     │
│  📝 Log Entry:                                                      │
│  "Found 0 task(s) + 1 approval(s) to process"                      │
│                                                                     │
│  Action: Invokes Qwen Code to process approvals                   │
└─────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│              STEP 11: QWEN EXECUTES APPROVAL                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ⏰ Time: 10:15 AM                                                  │
│                                                                     │
│  Qwen Code executes:                                                │
│  1. /process-approvals ← Executes approved actions                │
│  2. /process-tasks                                                  │
│                                                                     │
│  Qwen reads:                                                        │
│  ✓ Approved/APPROVAL_Email_Reply_client_abc123.md                  │
│  ✓ Extracts: to, subject, email body                               │
│  ✓ Verifies: Approval timestamp, human authorized                  │
│                                                                     │
│  Qwen executes:                                                     │
│  ✓ Uses Gmail API (or Email MCP)                                   │
│  ✓ Sends email to client@company.com                               │
│  ✓ Attaches invoice if specified                                   │
│                                                                     │
│  Action: Email sent via Gmail API                                  │
└─────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│              STEP 12: EMAIL SENT SUCCESSFULLY                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ⏰ Time: 10:15 AM                                                  │
│                                                                     │
│  📧 Email Sent:                                                     │
│  To: client@company.com                                            │
│  Subject: Re: Urgent: Need invoice for March services             │
│  Status: Delivered ✅                                              │
│                                                                     │
│  📝 Log Entry Created:                                              │
│  Logs/email_sent.json                                              │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ {                                                            │   │
│  │   "timestamp": "2026-04-01T10:15:00",                       │   │
│  │   "action": "email_sent",                                    │   │
│  │   "to": "client@company.com",                                │   │
│  │   "subject": "Re: Urgent: Need invoice for March services", │   │
│  │   "approved_by": "human",                                    │   │
│  │   "result": "success",                                       │   │
│  │   "message_id": "<abc123@gmail.com>"                        │   │
│  │ }                                                            │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  Action: Task moved to Done/ folder                                │
└─────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│              STEP 13: TASK MOVED TO DONE                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  📁 Folder: AI_Employee_Vault/Done/                                │
│                                                                     │
│  📄 File Moved:                                                     │
│  EMAIL_Urgent_Need_Invoice_abc123.md → Done/                       │
│  APPROVAL_Email_Reply_client_abc123.md → Done/                     │
│                                                                     │
│  Status: Complete with full audit trail                           │
│                                                                     │
│  Action: Dashboard updates with completion status                 │
└─────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│              STEP 14: DASHBOARD UPDATES (COMPLETE)                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  📁 File: AI_Employee_Vault/Dashboard.md                           │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ # AI Employee Dashboard                                     │   │
│  │                                                              │   │
│  │ ## System Status                                            │   │
│  │ - Status: Active                                            │   │
│  │ - Last Check: 2026-04-01 10:15                             │   │
│  │ - Pending Tasks: 0                                          │   │
│  │ - Completed Today: 1 ✅                                     │   │
│  │                                                              │   │
│  │ ## Recent Activity                                          │   │
│  │ - [2026-04-01 10:15] Email sent to client@company.com -     │   │
│  │   Invoice delivered successfully ✅                          │   │
│  │ - [2026-04-01 10:15] Approval executed: send_email          │   │
│  │ - [2026-04-01 10:10] Human approved: send_email             │   │
│  │ - [2026-04-01 10:05] Approval request created               │   │
│  │ - [2026-04-01 10:05] Email task created                     │   │
│  │                                                              │   │
│  │ ## Pending Actions                                          │   │
│  │ ✓ No pending actions                                        │   │
│  │                                                              │   │
│  │ ## Quick Stats                                              │   │
│  │ - Tasks in Queue: 0                                         │   │
│  │ - Awaiting Approval: 0                                      │   │
│  │ - Completed This Week: 1 ✅                                 │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ✅ COMPLETE - Full automation achieved!                           │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Timeline Summary

| Time | Event | Folder Status | Your Action |
|------|-------|---------------|-------------|
| 10:00 | Email arrives | Gmail Inbox | - |
| 10:01 | Watcher detects | → Needs_Action/ | - |
| 10:05 | Qwen processes | → Pending_Approval/ | - |
| 10:10 | You review | You move to Approved/ | **APPROVE** |
| 10:15 | Auto-executes | → Done/ | - |

**Total Time:** 15 minutes  
**Your Involvement:** 1 action (approve)  
**Automation:** Everything else automatic!

---

## Folder Movement Summary

```
Email Lifecycle:

Gmail Inbox
    ↓ (Gmail Watcher detects)
Needs_Action/EMAIL_*.md
    ↓ (Continuous Processor + Qwen)
Pending_Approval/APPROVAL_*.md
    ↓ (YOU move this)
Approved/APPROVAL_*.md
    ↓ (Continuous Processor + Qwen executes)
Done/ (email sent + logged)
```

---

## Key Points

### **What You Do:**
1. Monitor Dashboard.md (or get notified)
2. Review approval requests in Pending_Approval/
3. Move to Approved/ (to approve) or Rejected/ (to decline)
4. That's it!

### **What System Does Automatically:**
1. Detects emails (Gmail Watcher)
2. Creates tasks (Gmail Watcher)
3. Processes tasks (Continuous Processor + Qwen)
4. Creates approval requests (Qwen)
5. Executes approved actions (Continuous Processor + Qwen)
6. Sends emails (Gmail API)
7. Logs everything (Logs/)
8. Updates Dashboard (Dashboard.md)

---

## Commands You Need to Know

### **Check for pending approvals:**
```bash
dir AI_Employee_Vault\Pending_Approval
```

### **Approve an action:**
```bash
move AI_Employee_Vault\Pending_Approval\*.md AI_Employee_Vault\Approved\
```

### **View dashboard:**
```bash
type AI_Employee_Vault\Dashboard.md
```

### **Check logs:**
```bash
type AI_Employee_Vault\Logs\continuous_processor.log
```

---

## This is why we use Continuous Processor (not Orchestrator)

**Orchestrator:** 
- ❌ Doesn't check Approved/ folder
- ❌ Email would sit in Approved/ forever
- ❌ Requires you to manually run /process-approvals

**Continuous Processor:**
- ✅ Checks Approved/ automatically
- ✅ Executes approvals within 5 minutes
- ✅ Fully automatic end-to-end!

---

**Ready to test Gmail automation?** Let's start!
