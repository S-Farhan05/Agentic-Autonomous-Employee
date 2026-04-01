#!/usr/bin/env node
/**
 * Email MCP Server for Gmail
 * Allows Qwen Code to send emails via Gmail API
 */

const { Server } = require('@modelcontextprotocol/sdk/server/index.js');
const { StdioServerTransport } = require('@modelcontextprotocol/sdk/server/stdio.js');
const { google } = require('googleapis');
const fs = require('fs');
const path = require('path');

// Load Gmail credentials
const credentialsPath = process.env.GMAIL_CREDENTIALS || path.join(__dirname, 'credentials.json');
let credentials;

try {
  credentials = JSON.parse(fs.readFileSync(credentialsPath, 'utf8'));
} catch (error) {
  console.error('Error loading credentials:', error.message);
  process.exit(1);
}

// Create MCP server
const server = new Server(
  {
    name: 'email-mcp',
    version: '1.0.0',
  },
  {
    capabilities: {
      resources: {},
      tools: {},
    },
  }
);

// Tool: Send Email
server.setRequestHandler('tools/call', async (request) => {
  const { name, arguments: args } = request.params;

  if (name === 'send_email') {
    try {
      const { to, subject, body, cc, bcc, attachments } = args;

      // Validate required fields
      if (!to || !subject || !body) {
        throw new Error('Missing required fields: to, subject, body');
      }

      // Authenticate with Gmail
      const auth = await getGmailAuth();
      const gmail = google.gmail({ version: 'v1', auth });

      // Create email message
      const message = createEmailMessage(to, subject, body, cc, bcc, attachments);

      // Send email
      const response = await gmail.users.messages.send({
        userId: 'me',
        requestBody: message,
      });

      return {
        content: [
          {
            type: 'text',
            text: `✅ Email sent successfully!\n\nTo: ${to}\nSubject: ${subject}\nMessage ID: ${response.data.id}\nThread ID: ${response.data.threadId}`,
          },
        ],
      };
    } catch (error) {
      return {
        content: [
          {
            type: 'text',
            text: `❌ Error sending email: ${error.message}`,
          },
        ],
        isError: true,
      };
    }
  }

  if (name === 'draft_email') {
    try {
      const { to, subject, body, cc, bcc } = args;

      if (!to || !subject || !body) {
        throw new Error('Missing required fields: to, subject, body');
      }

      const auth = await getGmailAuth();
      const gmail = google.gmail({ version: 'v1', auth });

      const message = createEmailMessage(to, subject, body, cc, bcc);

      const response = await gmail.users.drafts.create({
        userId: 'me',
        requestBody: message,
      });

      return {
        content: [
          {
            type: 'text',
            text: `✅ Draft email created!\n\nTo: ${to}\nSubject: ${subject}\nDraft ID: ${response.data.id}`,
          },
        ],
      };
    } catch (error) {
      return {
        content: [
          {
            type: 'text',
            text: `❌ Error creating draft: ${error.message}`,
          },
        ],
        isError: true,
      };
    }
  }

  throw new Error(`Unknown tool: ${name}`);
});

// List available tools
server.setRequestHandler('tools/list', async () => {
  return {
    tools: [
      {
        name: 'send_email',
        description: 'Send an email via Gmail API. Requires approval before sending.',
        inputSchema: {
          type: 'object',
          properties: {
            to: { type: 'string', description: 'Recipient email address' },
            subject: { type: 'string', description: 'Email subject' },
            body: { type: 'string', description: 'Email body (plain text or HTML)' },
            cc: { type: 'string', description: 'CC recipients (comma-separated)' },
            bcc: { type: 'string', description: 'BCC recipients (comma-separated)' },
            attachments: {
              type: 'array',
              items: { type: 'string' },
              description: 'Paths to attachment files',
            },
          },
          required: ['to', 'subject', 'body'],
        },
      },
      {
        name: 'draft_email',
        description: 'Create a draft email in Gmail (does not send)',
        inputSchema: {
          type: 'object',
          properties: {
            to: { type: 'string', description: 'Recipient email address' },
            subject: { type: 'string', description: 'Email subject' },
            body: { type: 'string', description: 'Email body' },
            cc: { type: 'string', description: 'CC recipients' },
            bcc: { type: 'string', description: 'BCC recipients' },
          },
          required: ['to', 'subject', 'body'],
        },
      },
    ],
  };
});

// Helper: Create Gmail auth with OAuth2
async function getGmailAuth() {
  const oauth2Client = new google.auth.OAuth2(
    credentials.installed.client_id,
    credentials.installed.client_secret,
    credentials.installed.redirect_uris[0]
  );

  // Try to load existing token
  const tokenPath = path.join(path.dirname(credentialsPath), 'token.pickle');
  
  try {
    const token = JSON.parse(fs.readFileSync(tokenPath, 'utf8'));
    oauth2Client.setCredentials(token);
    
    // Refresh token if expired
    try {
      await oauth2Client.getAccessToken();
    } catch (error) {
      throw new Error('Token expired. Please re-authenticate.');
    }
    
    return oauth2Client;
  } catch (error) {
    throw new Error('Authentication token not found or invalid. Please run authentication first.');
  }
}

// Helper: Create RFC 2822 email message
function createEmailMessage(to, subject, body, cc, bcc, attachments) {
  let headers = [
    `To: ${to}`,
    `Subject: ${subject}`,
    `MIME-Version: 1.0`,
    `Content-Type: multipart/alternative; boundary="BOUNDARY"`,
  ];

  if (cc) headers.push(`Cc: ${cc}`);

  let email = headers.join('\r\n') + '\r\n\r\n';
  email += '--BOUNDARY\r\n';
  email += 'Content-Type: text/plain; charset="UTF-8"\r\n\r\n';
  email += body + '\r\n\r\n';
  email += '--BOUNDARY\r\n';
  email += 'Content-Type: text/html; charset="UTF-8"\r\n\r\n';
  email += `<body>${body.replace(/\n/g, '<br>')}</body>\r\n\r\n`;
  email += '--BOUNDARY--';

  const encodedMessage = Buffer.from(email)
    .toString('base64')
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=+$/, '');

  return {
    raw: encodedMessage,
  };
}

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('Email MCP Server running on stdio');
}

main().catch((error) => {
  console.error('Fatal error:', error);
  process.exit(1);
});
