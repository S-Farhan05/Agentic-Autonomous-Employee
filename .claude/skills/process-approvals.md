---
name: process-approvals
description: Handle human-in-the-loop approval workflow for sensitive actions
trigger: /process-approvals
---

# Process Approvals Skill

This skill manages the approval workflow for sensitive actions that require human review before execution.

## What This Skill Does

1. Checks Pending_Approval folder for approval requests
2. Presents requests to user for review
3. Processes approved actions via appropriate MCP servers
4. Logs all approval decisions
5. Updates Dashboard with approval status
6. Moves completed approvals to Done folder

## Usage

```bash
/process-approvals
```

Or check specific approval:

```bash
/process-approvals --id APPROVAL_email_client_a
```

## Instructions for Claude

When this skill is invoked:

1. **Scan Pending_Approval Folder**
   - Read all files in AI_Employee_Vault/Pending_Approval/
   - Parse frontmatter for action type and details
   - Check expiration dates
   - Prioritize by urgency

2. **Check for Approved Actions**
   - Scan AI_Employee_Vault/Approved/ folder
   - These are approvals the human has moved from Pending_Approval
   - Ready for execution

3. **Execute Approved Actions**

   For each file in Approved/:

   **Email Actions:**
   ```markdown
   # Read: Approved/EMAIL_client_a.md
   ---
   action: send_email
   to: client@example.com
   subject: Invoice for March
   attachment: /Vault/Invoices/march.pdf
   approved_by: human
   approved_at: 2026-03-31T10:00:00Z
   ---
   ```

   Execute:
   - Use email MCP server to send
   - Log to Logs/email_sent.json
   - Move to Done/
   - Update Dashboard

   **Payment Actions:**
   ```markdown
   # Read: Approved/PAYMENT_vendor_x.md
   ---
   action: payment
   amount: 500.00
   recipient: Vendor X
   reference: Invoice #1234
   approved_by: human
   ---
   ```

   Execute:
   - Use payment MCP server
   - Log transaction
   - Move to Done/
   - Update accounting records

   **Social Media Actions:**
   ```markdown
   # Read: Approved/POST_linkedin_123.md
   ---
   action: post_linkedin
   content: "Excited to announce..."
   approved_by: human
   ---
   ```

   Execute:
   - Use LinkedIn MCP/API
   - Log post
   - Move to Done/

4. **Check for Rejected Actions**
   - Scan AI_Employee_Vault/Rejected/ folder
   - Log rejection reason
   - Move to Done/ with rejection note
   - Update Dashboard

5. **Handle Expired Approvals**
   - Check expiration dates in Pending_Approval
   - If expired (> 24 hours), move to Rejected
   - Notify in Dashboard

6. **Update Dashboard**
   - Show pending approval count
   - List urgent approvals
   - Log executed actions
   - Alert on expired requests

## Approval Request Format

When creating approval requests (from other skills):

```markdown
# /Vault/Pending_Approval/[ACTION]_[identifier].md
---
type: approval_request
action: [send_email|payment|post_social|delete_file]
priority: [high|medium|low]
created: [timestamp]
expires: [timestamp]
status: pending
---

## Action Details
[Clear description of what will happen]

## Context
[Why this action is needed]

## To Approve
Move this file to /Approved folder

## To Reject
Move this file to /Rejected folder

## Risk Assessment
[Potential issues or concerns]
```

## Safety Rules

- NEVER execute actions from Pending_Approval directly
- ONLY execute from Approved folder
- ALWAYS log approval decisions
- ALWAYS verify action details before execution
- Check expiration dates
- Validate approval authority

## Example Workflow

**1. Approval Request Created:**
```
/Pending_Approval/EMAIL_invoice_client_a.md
```

**2. Human Reviews and Approves:**
```
User moves file to: /Approved/EMAIL_invoice_client_a.md
```

**3. Claude Processes:**
```bash
/process-approvals
# Detects file in Approved/
# Executes email send via MCP
# Logs action
# Moves to Done/
```

**4. Dashboard Updated:**
```
Recent Activity:
- [2026-03-31 10:15] Email sent to Client A - Invoice delivered
```

## Integration with MCP Servers

This skill coordinates with:
- **Email MCP**: For sending emails
- **Payment MCP**: For financial transactions
- **Social Media MCP**: For posting content
- **Browser MCP**: For web-based actions

## Output Format

After processing:

```
Processed approvals:
- X actions executed from Approved/
- Y requests still pending in Pending_Approval/
- Z requests expired and moved to Rejected/

Urgent approvals waiting:
- [List of high-priority pending approvals]

Dashboard updated.
```

## Error Handling

- If MCP server fails, move back to Pending_Approval
- Log error details
- Alert in Dashboard
- Don't retry automatically (requires new approval)
