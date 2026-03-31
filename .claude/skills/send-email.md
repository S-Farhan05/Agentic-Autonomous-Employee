---
name: send-email
description: Send emails via MCP server with approval workflow
trigger: /send-email
---

# Send Email Skill

This skill handles email sending through MCP server integration with proper approval workflow.

## What This Skill Does

1. Drafts professional emails based on context
2. Creates approval requests for human review
3. Sends approved emails via Email MCP server
4. Logs all email activities
5. Updates Dashboard with email status
6. Handles attachments and formatting

## Usage

```bash
/send-email --to "client@example.com" --subject "Invoice" --draft
```

Or process from approval:

```bash
/send-email --from-approval EMAIL_client_a
```

## Instructions for Claude

When this skill is invoked:

1. **Draft Email Mode**

   If creating a new email:

   a. **Gather Context**
   - Read Company_Handbook.md for tone and style
   - Check if recipient is known (search vault)
   - Understand the purpose (invoice, follow-up, inquiry)

   b. **Draft Email**
   ```
   To: [recipient]
   Subject: [clear, professional subject]

   [Greeting based on relationship]

   [Body - clear, concise, professional]

   [Call to action if needed]

   [Professional closing]
   [Your name/company]
   ```

   c. **Create Approval Request**
   ```markdown
   # Pending_Approval/EMAIL_[identifier].md
   ---
   type: approval_request
   action: send_email
   to: client@example.com
   subject: Invoice for March Services
   has_attachment: true
   attachment_path: /Vault/Invoices/march.pdf
   priority: medium
   created: 2026-03-31T10:00:00Z
   expires: 2026-04-01T10:00:00Z
   ---

   ## Email Draft

   **To:** client@example.com
   **Subject:** Invoice for March Services
   **Attachment:** march.pdf

   ---

   Dear [Client Name],

   [Email body]

   Best regards,
   [Your name]

   ---

   ## Context
   This email sends the March invoice to Client A as requested.

   ## To Approve
   Move this file to /Approved folder

   ## To Reject
   Move this file to /Rejected folder
   ```

2. **Send Approved Email**

   When processing from Approved folder:

   a. **Read Approval File**
   - Parse email details
   - Verify approval timestamp
   - Check attachment exists

   b. **Send via MCP**
   ```python
   # Pseudo-code for MCP integration
   email_mcp.send_email({
       'to': recipient,
       'subject': subject,
       'body': body,
       'attachments': [attachment_path]
   })
   ```

   c. **Log Activity**
   ```json
   {
     "timestamp": "2026-03-31T10:15:00Z",
     "action": "email_sent",
     "to": "client@example.com",
     "subject": "Invoice for March Services",
     "approved_by": "human",
     "result": "success",
     "message_id": "abc123"
   }
   ```

   d. **Update Dashboard**
   - Add to Recent Activity
   - Update email stats
   - Clear from pending approvals

3. **Handle Attachments**
   - Verify file exists in vault
   - Check file size (< 25MB)
   - Validate file type
   - Include in MCP call

4. **Error Handling**
   - If MCP fails, log error
   - Move back to Pending_Approval
   - Add error note to Dashboard
   - Don't retry automatically

## Email Templates

### Invoice Email
```
Subject: Invoice [#Number] - [Month] Services

Dear [Client Name],

Please find attached the invoice for [services] provided during [period].

Invoice Details:
- Amount: $[amount]
- Due Date: [date]
- Services: [description]

Payment can be made via [payment methods].

Please let me know if you have any questions.

Best regards,
[Your name]
```

### Follow-up Email
```
Subject: Following up on [Topic]

Hi [Name],

I wanted to follow up on [previous topic/email].

[Context and update]

[Next steps or call to action]

Looking forward to hearing from you.

Best regards,
[Your name]
```

### Client Inquiry Response
```
Subject: Re: [Original Subject]

Hi [Name],

Thank you for reaching out about [topic].

[Answer to inquiry]

[Additional helpful information]

Please let me know if you need anything else.

Best regards,
[Your name]
```

## MCP Server Configuration

Requires email MCP server configured in Claude Code settings:

```json
{
  "mcpServers": {
    "email": {
      "command": "node",
      "args": ["path/to/email-mcp/index.js"],
      "env": {
        "GMAIL_CREDENTIALS": "path/to/credentials.json"
      }
    }
  }
}
```

## Safety Rules

- NEVER send email without approval
- ALWAYS create approval request first
- VERIFY recipient email address
- CHECK for sensitive information
- LOG all sent emails
- VALIDATE attachments exist

## Output Format

**Draft Mode:**
```
Email draft created: EMAIL_[identifier].md

To: client@example.com
Subject: Invoice for March Services
Status: Pending approval in /Pending_Approval

Move to /Approved to send.
```

**Send Mode:**
```
Email sent successfully!

To: client@example.com
Subject: Invoice for March Services
Sent at: 2026-03-31 10:15
Message ID: abc123

Logged to: Logs/2026-03-31_email.json
Dashboard updated.
```

## Integration Points

- **Company_Handbook.md**: Email tone and style guidelines
- **Email MCP Server**: Actual sending mechanism
- **Approval Workflow**: Human-in-the-loop for safety
- **Dashboard**: Activity tracking
- **Logs**: Audit trail
