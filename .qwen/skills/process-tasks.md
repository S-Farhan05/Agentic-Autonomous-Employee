---
name: process-tasks
description: Process pending tasks from the AI Employee vault
trigger: /process-tasks
---

# Process Tasks Skill

This skill processes pending tasks from the Needs_Action folder according to the Company Handbook rules.

## What This Skill Does

1. Reads all files in the Needs_Action folder
2. Analyzes each task based on Company_Handbook.md rules
3. Determines priority and required actions
4. Creates plans for complex tasks
5. Executes auto-approved actions
6. Creates approval requests for sensitive actions
7. Updates Dashboard.md with current status
8. Moves completed tasks to Done folder

## Usage

```bash
/process-tasks
```

Or with specific options:

```bash
/process-tasks --priority high
/process-tasks --dry-run
```

## Instructions for Claude

When this skill is invoked:

1. **Read the Company Handbook**
   - Load AI_Employee_Vault/Company_Handbook.md
   - Understand the rules and decision authority levels
   - Key rule: NEVER send emails/messages without human approval

2. **Check Needs_Action Folder**
   - Read all .md files in AI_Employee_Vault/Needs_Action/
   - Parse the frontmatter to understand task type and priority
   - Focus on type: email files first

3. **Process Each Task**

   **For EMAIL tasks (type: email):**
   - Read the email content
   - Determine if a reply is needed:
     * Greeting/intro email → Reply needed
     * Question asked → Reply needed  
     * Request for information → Reply needed
     * Invoice request → Reply needed with invoice
   - **CRITICAL: If reply needed, create approval request in Pending_Approval/**
   - Draft a professional response
   - Create approval request file with this format:

   ```markdown
   ---
   type: approval_request
   action: send_email
   to: {sender_email}
   subject: Re: {original_subject}
   priority: medium
   created: {timestamp}
   expires: {timestamp+24h}
   status: pending
   ---

   ## Email Draft

   **To:** {sender}
   **Subject:** Re: {subject}

   ---

   {Draft email body here}

   ---

   ## Context
   {Why this reply is needed}

   ## To Approve
   Move this file to /Approved folder

   ## To Reject  
   Move this file to /Rejected folder
   ```

   **For auto-approved tasks:**
   - Reading/categorizing emails
   - Creating draft responses
   - Organizing files
   - Generating reports
   - Log the action and move to Done/

   **For approval-required tasks:**
   - Sending any email or message
   - Making any payment
   - Posting to social media
   - Create detailed approval request in Pending_Approval/
   - Include all relevant context
   - Wait for human to move to Approved/

4. **Create Plans for Complex Tasks**
   - If task requires multiple steps, create a Plan.md file in Plans/
   - Use checkbox format for tracking progress
   - Include estimated time and dependencies

5. **Update Dashboard**
   - Update AI_Employee_Vault/Dashboard.md
   - Add recent activity
   - Update pending actions count
   - Update quick stats
   - List any new approval requests created

6. **Handle Errors Gracefully**
   - If uncertain, create an approval request
   - Log all errors to Logs/
   - Never guess on critical matters

## Example Task Processing Flow

### Email Task Example
```markdown
# Input: Needs_Action/EMAIL_12345.md
---
type: email
from: client@example.com
subject: Invoice Request
priority: high
---

Client is asking for January invoice.
```

**Processing Steps:**
1. Identify task type: email response
2. Check handbook: Email responses require approval
3. Draft response
4. Create approval request in Pending_Approval/
5. Update Dashboard with pending approval

### File Drop Example
```markdown
# Input: Needs_Action/FILE_document.pdf.md
---
type: file_drop
original_name: document.pdf
size: 245.67 KB
---

New file dropped for processing.
```

**Processing Steps:**
1. Identify task type: file processing
2. Read file contents (if text-based)
3. Determine appropriate action
4. Create plan if complex processing needed
5. Update Dashboard

## Priority Handling

**High Priority** (Process immediately)
- Tasks with priority: high in frontmatter
- Keywords: urgent, asap, emergency
- Client requests
- Payment reminders

**Medium Priority** (Process within 24 hours)
- Regular business tasks
- Routine emails
- File processing

**Low Priority** (Process when convenient)
- Newsletters
- Non-critical notifications
- Cleanup tasks

## Safety Rules

- NEVER send emails without approval
- NEVER make payments without approval
- NEVER delete files without approval
- ALWAYS log actions
- ALWAYS update Dashboard
- When in doubt, ask for approval

## Output Format

After processing, provide a summary:

```
Processed X tasks:
- Y completed automatically
- Z require approval
- A moved to Done

Dashboard updated.
Next check recommended in: [timeframe]
```
