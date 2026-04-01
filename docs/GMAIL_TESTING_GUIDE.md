# Gmail Automation Testing Guide

**Date:** 2026-04-01  
**Status:** ⏳ **READY FOR TESTING**

---

## Prerequisites Checklist

Before testing Gmail automation, verify:

- [x] Python dependencies installed
- [x] `credentials.json` present in `credentials/` folder
- [ ] Gmail API enabled in Google Cloud Console
- [ ] OAuth2 consent screen configured
- [ ] Test email account ready

---

## Step-by-Step Testing Guide

### **Step 1: Verify Credentials File**

Check that `credentials/credentials.json` exists:

```bash
dir credentials\credentials.json
```

**Expected Output:**
```
credentials.json file found
```

**Status:** ✅ **Already present** (from previous setup)

---

### **Step 2: First Run - OAuth2 Authentication**

The first run requires you to authenticate with Google:

```bash
cd E:\Farhan-work\Hackathon\Agentic-Autonomous-Employee
python watchers/gmail_watcher.py
```

**What Happens:**

1. **Browser Opens Automatically**
   - Opens to Google OAuth2 consent screen
   - URL: `https://accounts.google.com/o/oauth2/...`

2. **Log In to Google**
   - Select your Gmail account
   - Review permissions requested:
     - "Read your Gmail messages"
     - This is READ-ONLY (secure)

3. **Grant Permissions**
   - Click "Allow" or "Continue"
   - Browser shows: "Authentication successful"
   - Browser may close automatically

4. **Token Saved**
   - File created: `credentials/token.pickle`
   - Contains: Access token + refresh token
   - Saved for future use (no re-auth needed)

5. **Watcher Starts Running**
   ```
   GmailWatcher - INFO - Gmail authentication successful
   GmailWatcher - INFO - ============================================================
   GmailWatcher - INFO - GMAIL WATCHER STARTED
   GmailWatcher - INFO - ============================================================
   GmailWatcher - INFO - Monitoring Gmail inbox
   GmailWatcher - INFO - Check interval: 120 seconds
   ```

**Troubleshooting:**

| Issue | Solution |
|-------|----------|
| Browser doesn't open | Check console for URL, open manually |
| "App not verified" | Click "Advanced" → "Go to (unsafe)" |
| Authentication failed | Delete `token.pickle`, try again |
| Port already in use | Use different port: `flow.run_local_server(port=8080)` |

---

### **Step 3: Send Test Email**

While watcher is running, send a test email:

**Option A: From Another Email Account**

1. Open Gmail in browser or email client
2. Compose new email to your monitored account
3. **Subject:** `Test: AI Employee Automation`
4. **Body:**
   ```
   This is a test email to verify Gmail watcher is working.
   
   Please process this email.
   ```
5. Send

**Option B: Use Gmail API to Send Test Email**

```bash
python -c "
import smtplib
from email.mime.text import MIMEText

# Send test email to yourself
msg = MIMEText('Test email for Gmail watcher')
msg['Subject'] = 'Test: AI Employee Automation'
msg['From'] = 'your_email@gmail.com'
msg['To'] = 'your_email@gmail.com'

# Send via SMTP (use app password if 2FA enabled)
# server = smtplib.SMTP('smtp.gmail.com', 587)
# server.starttls()
# server.login('your_email', 'app_password')
# server.send_message(msg)
# server.quit()
"
```

**Option C: Use a Friend's Email**

Ask a friend to send you an email with subject containing:
- "urgent"
- "asap"
- "invoice"
- "test"

---

### **Step 4: Watch for Task Creation**

**Monitor the Watcher Terminal:**

Within 2 minutes (check interval), you should see:

```
GmailWatcher - INFO - Found 1 new email(s)
GmailWatcher - INFO - Created task for email: Test: AI Employee Automation
```

**Check Needs_Action Folder:**

```bash
dir AI_Employee_Vault\Needs_Action
```

**Expected:** New file created:
```
EMAIL_Test_AI_Employee_Automation_abc123.md
```

---

### **Step 5: Verify Task File Content**

Open the created task file:

```bash
type AI_Employee_Vault\Needs_Action\EMAIL_Test_AI_Employee_Automation_*.md
```

**Expected Content:**

```markdown
---
type: email
from: sender@example.com
subject: Test: AI Employee Automation
received: 2026-04-01T10:00:00
priority: medium
status: pending
gmail_id: abc123
---

## Email from sender@example.com

**Subject:** Test: AI Employee Automation
**Date:** Wed, 01 Apr 2026 10:00:00 +0000
**Priority:** medium

## Email Content

This is a test email to verify Gmail watcher is working.

Please process this email.

## Suggested Actions
- [ ] Read full email
- [ ] Draft response
- [ ] Create approval request if reply needed
- [ ] Move to Done when processed
```

---

### **Step 6: Test Priority Detection**

Send another email with urgent keywords:

**Subject:** `URGENT: Invoice needed ASAP`

**Expected:**
```bash
# Task created with priority: high
---
priority: high
---
```

**Keywords that trigger HIGH priority:**
- urgent
- asap
- important
- invoice

---

### **Step 7: Test Continuous Processing**

Now test the full automation loop:

**1. Start Continuous Processor:**

```bash
# In separate terminal
python scripts/continuous_processor.py
```

**2. Send Test Email:**

Subject: `Test: Please reply`

**3. Wait for Processing Cycle (5 minutes):**

Continuous processor will:
- Detect task in Needs_Action/
- Invoke Qwen Code
- Qwen processes email
- Creates approval request (if reply needed)

**4. Check Dashboard:**

```bash
type AI_Employee_Vault\Dashboard.md
```

**Expected Update:**

```markdown
## Recent Activity
- [2026-04-01 10:05] Email task created: Test: Please reply
- [2026-04-01 10:05] Processing started by Qwen
```

---

### **Step 8: Test Approval Workflow**

If Qwen creates an approval request:

**1. Check Pending_Approval Folder:**

```bash
dir AI_Employee_Vault\Pending_Approval
```

**Expected:**
```
APPROVAL_Email_Reply_test_123.md
```

**2. Review Approval Request:**

```bash
type AI_Employee_Vault\Pending_Approval\APPROVAL_Email_Reply_test_123.md
```

**Content:**
```markdown
---
type: approval_request
action: send_email
to: sender@example.com
subject: Re: Test: Please reply
---

## Email Draft

Dear Sender,

Thank you for your email...

[Draft response]

## To Approve
Move this file to /Approved folder
```

**3. Human Decision Time:**

**Option A: Approve**
```bash
move AI_Employee_Vault\Pending_Approval\APPROVAL_*.md AI_Employee_Vault\Approved\
```

**Option B: Reject**
```bash
move AI_Employee_Vault\Pending_Approval\APPROVAL_*.md AI_Employee_Vault\Rejected\
```

**Option C: Edit then Approve**
```bash
# Edit file in text editor
notepad AI_Employee_Vault\Pending_Approval\APPROVAL_*.md

# Then move to Approved
move AI_Employee_Vault\Pending_Approval\APPROVAL_*.md AI_Employee_Vault\Approved\
```

**4. Wait for Next Processing Cycle (5 minutes):**

Continuous processor will:
- Detect approval in Approved/
- Execute action (send email)
- Move to Done/
- Update Dashboard

---

## Test Scenarios

### **Test 1: Basic Email Detection** ✅

**Send:** Regular email  
**Expected:** Task created with priority: medium  
**Verify:** File in Needs_Action/

---

### **Test 2: High Priority Email** ✅

**Send:** Email with "urgent" or "asap" in subject  
**Expected:** Task created with priority: high  
**Verify:** Frontmatter shows `priority: high`

---

### **Test 3: Invoice Email** ✅

**Send:** Email with "invoice" in subject  
**Expected:** Task created with priority: high  
**Verify:** Correctly categorized

---

### **Test 4: Email with Attachment** ⏳

**Send:** Email with PDF attachment  
**Expected:** Task mentions attachment  
**Verify:** Attachment info in task file

---

### **Test 5: Multiple Emails** ⏳

**Send:** 3 emails at once  
**Expected:** 3 tasks created  
**Verify:** All 3 in Needs_Action/

---

### **Test 6: Already Processed** ⏳

**Wait:** 5 minutes, don't mark as read  
**Expected:** No duplicate tasks  
**Verify:** processed_ids prevents duplicates

---

## Common Issues & Solutions

### Issue 1: Authentication Fails

**Error:**
```
google.auth.exceptions.RefreshError: The credentials do not contain the necessary fields
```

**Solution:**
```bash
# Delete old token
del credentials\token.pickle

# Re-run authentication
python watchers/gmail_watcher.py
```

---

### Issue 2: No Emails Detected

**Possible Causes:**
1. No unread emails
2. Query too restrictive
3. API quota exceeded

**Solutions:**

**Check for unread emails:**
```bash
# Manually check Gmail
# Look for unread emails
```

**Modify query (if needed):**
Edit `watchers/gmail_watcher.py`:

```python
# Line ~130, change query to:
q='is:unread'  # Simpler query for testing
```

---

### Issue 3: Task Not Created

**Possible Causes:**
1. Needs_Action folder doesn't exist
2. Permission denied
3. Script error

**Solutions:**

**Check folder exists:**
```bash
dir AI_Employee_Vault\Needs_Action
```

**Check permissions:**
```bash
# Try creating file manually
echo test > AI_Employee_Vault\Needs_Action\test.txt
del AI_Employee_Vault\Needs_Action\test.txt
```

**Check logs:**
```bash
type AI_Employee_Vault\Logs\gmail_watcher.log
```

---

### Issue 4: Watcher Crashes

**Error:**
```
Exception in GmailWatcher
```

**Solution:**
```bash
# Check log for details
type AI_Employee_Vault\Logs\gmail_watcher.log

# Restart watcher
python watchers/gmail_watcher.py
```

---

## Success Criteria

Gmail automation test is successful when:

- [ ] Watcher starts without errors
- [ ] Authentication completes
- [ ] Test email sent
- [ ] Task created in Needs_Action/ within 2 minutes
- [ ] Task file has correct format
- [ ] Priority correctly assigned
- [ ] No duplicate tasks created
- [ ] Dashboard updates
- [ ] Logs show all activities

---

## Performance Metrics to Monitor

| Metric | Expected | Acceptable Range |
|--------|----------|------------------|
| Detection time | < 2 minutes | < 5 minutes |
| Task creation | < 5 seconds | < 10 seconds |
| File size | ~1 KB | 0.5-2 KB |
| Memory usage | ~50 MB | < 100 MB |
| CPU usage | < 1% | < 5% |

---

## Next Steps After Testing

### If Test Successful ✅

1. **Configure Production Settings:**
   - Adjust check interval (currently 2 minutes)
   - Modify email query if needed
   - Add custom keywords

2. **Set Up Automatic Start:**
   - Windows Task Scheduler
   - Run on system startup

3. **Test Other Watchers:**
   - WhatsApp watcher
   - File watcher (already tested)

4. **Test Full Workflow:**
   - Email → Task → Approval → Reply → Done

---

### If Test Fails ❌

1. **Debug:**
   - Check logs
   - Verify credentials
   - Test with simpler query

2. **Fix Issues:**
   - Update code if needed
   - Re-authenticate
   - Check API quotas

3. **Retry:**
   - Start fresh
   - Follow steps again

---

## Quick Start Commands

### **Start Gmail Watcher:**
```bash
python watchers/gmail_watcher.py
```

### **Send Test Email:**
From another account, send to your Gmail:
- Subject: `Test: AI Employee`
- Body: `Testing Gmail automation`

### **Check for Task:**
```bash
dir AI_Employee_Vault\Needs_Action\EMAIL_*.md
```

### **View Task Content:**
```bash
type AI_Employee_Vault\Needs_Action\EMAIL_*.md
```

### **Check Logs:**
```bash
type AI_Employee_Vault\Logs\gmail_watcher.log
```

### **View Dashboard:**
```bash
type AI_Employee_Vault\Dashboard.md
```

---

## Test Log Template

Use this to track your test:

```
=== Gmail Automation Test Log ===
Date: 2026-04-01
Tester: [Your name]

[ ] Step 1: Credentials verified
[ ] Step 2: Authentication successful
[ ] Step 3: Test email sent
[ ] Step 4: Task created (time: __:__)
[ ] Step 5: Task content verified
[ ] Step 6: Priority detection tested
[ ] Step 7: Continuous processing tested
[ ] Step 8: Approval workflow tested

Issues encountered:
1. 
2. 
3. 

Overall result: PASS / FAIL
Notes:
```

---

**Ready to test? Let me know when you want to start!**
