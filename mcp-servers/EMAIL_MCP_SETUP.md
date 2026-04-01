# Email MCP Server Setup Guide

**Purpose:** Enable automatic email sending via MCP (Model Context Protocol)

---

## What is Email MCP?

MCP (Model Context Protocol) allows Qwen Code to send emails programmatically through a standardized interface.

---

## Option 1: Use Anthropic's Email MCP (Recommended)

### **Install Email MCP Server**

```bash
npm install -g @anthropic/email-mcp
```

### **Configure for Qwen Code**

Create or edit Qwen Code MCP config:

**File:** `%APPDATA%\Claude\claude_desktop_config.json` (Windows)
**Or:** `~/.config/claude/claude_desktop_config.json` (Mac/Linux)

```json
{
  "mcpServers": {
    "email": {
      "command": "npx",
      "args": ["-y", "@anthropic/email-mcp"],
      "env": {
        "GMAIL_CREDENTIALS": "E:\\Farhan-work\\Hackathon\\Agentic-Autonomous-Employee\\credentials\\credentials.json"
      }
    }
  }
}
```

### **Restart Qwen Code**

After adding the config, restart Qwen Code for changes to take effect.

### **Test Email MCP**

In Qwen Code:

```
/send-email --to "your-email@gmail.com" --subject "Test" --draft
```

---

## Option 2: Use Gmail API Directly (Simpler for Testing)

For Silver Tier testing, we can use Gmail API directly without MCP.

The `/send-email` skill already supports this approach.

### **How It Works**

1. Qwen creates approval request in `Pending_Approval/`
2. You approve (move to `Approved/`)
3. Qwen uses Gmail API to send email
4. No MCP server needed!

### **Requirements**

- Gmail API credentials (already have: `credentials/credentials.json`)
- Gmail API scopes for sending (need to add)

### **Add Sending Scopes**

Update the Gmail watcher to request sending permissions:

**File:** `watchers/gmail_watcher.py`

Change line ~18:

```python
# OLD (read-only):
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# NEW (read + send):
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.compose'
]
```

Then re-authenticate:

```bash
del credentials\token.pickle
python scripts/test_gmail_auth.py
```

---

## Option 3: Custom Email MCP Server (Advanced)

Create a simple Node.js MCP server for email:

### **Create MCP Server**

```bash
mkdir mcp-servers\email-mcp
cd mcp-servers\email-mcp
npm init -y
npm install @modelcontextprotocol/server
```

### **Create index.js**

```javascript
#!/usr/bin/env node
const { Server } = require('@modelcontextprotocol/server');
const { google } = require('googleapis');
const fs = require('fs');

const server = new Server({
  name: 'email-mcp',
  version: '1.0.0',
});

server.setRequestHandler('email/send', async (request) => {
  const { to, subject, body, attachments } = request.params;
  
  // Load credentials
  const credentials = JSON.parse(
    fs.readFileSync(process.env.GMAIL_CREDENTIALS, 'utf8')
  );
  
  // Authenticate and send
  // ... (implementation)
  
  return { success: true, messageId: '...' };
});

server.run();
```

### **Configure in Qwen**

```json
{
  "mcpServers": {
    "email": {
      "command": "node",
      "args": ["E:\\Farhan-work\\Hackathon\\Agentic-Autonomous-Employee\\mcp-servers\\email-mcp\\index.js"],
      "env": {
        "GMAIL_CREDENTIALS": "E:\\Farhan-work\\Hackathon\\Agentic-Autonomous-Employee\\credentials\\credentials.json"
      }
    }
  }
}
```

---

## Recommendation for Testing

**For now, use Option 2 (Gmail API directly)** because:

1. ✅ No additional setup needed
2. ✅ Already supported by `/send-email` skill
3. ✅ Works with approval workflow
4. ✅ No MCP server installation required

**Later, add MCP server** for production use.

---

## Quick Test (Without MCP)

Once Gmail OAuth is configured:

1. **Run watchers:**
   ```bash
   python watchers/gmail_watcher.py
   python scripts/continuous_processor.py
   ```

2. **Send test email to your Gmail:**
   - Subject: "Test: Please reply"
   - Body: "Can you test the email automation?"

3. **Watch automation:**
   - Task created in `Needs_Action/` (2 min)
   - Approval request in `Pending_Approval/` (5 min)
   - You approve (move to `Approved/`)
   - Email sends automatically (5 min)

4. **Check logs:**
   ```bash
   type AI_Employee_Vault\Logs\gmail_watcher.log
   type AI_Employee_Vault\Logs\continuous_processor.log
   ```

---

## Troubleshooting

### **Issue: MCP server not found**

```bash
# Install globally
npm install -g @anthropic/email-mcp
```

### **Issue: Gmail API permission denied**

Re-authenticate with sending scopes:

```bash
del credentials\token.pickle
python scripts/test_gmail_auth.py
```

### **Issue: Email not sending**

Check logs:
```bash
type AI_Employee_Vault\Logs\email_sent.log
```

---

## Next Steps

1. ✅ Complete OAuth consent screen setup
2. ✅ Test Gmail watcher (read emails)
3. ⏳ Add sending scopes and re-authenticate
4. ⏳ Test email sending with approval workflow
5. ⏳ (Optional) Set up MCP server for production
