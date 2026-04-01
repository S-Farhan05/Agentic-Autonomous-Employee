#!/usr/bin/env python3
"""
Send Approved Email

This script sends emails that have been approved in the Approved folder.
It reads the approval request, sends via Gmail API, and moves to Done.

Usage: python send_approved_email.py <approval_file_path> [vault_path]
"""

import sys
import base64
import re
from pathlib import Path
from datetime import datetime
from email.mime.text import MIMEText

def extract_frontmatter(content):
    """Extract frontmatter from markdown file"""
    match = re.search(r'^---\s*\n(.*?)\n---\s*$', content, re.DOTALL)
    if not match:
        return {}, content

    frontmatter = {}
    for line in match.group(1).split('\n'):
        if ':' in line:
            idx = line.index(':')
            key = line[:idx].strip()
            value = line[idx+1:].strip()
            frontmatter[key] = value

    body = content[match.end():].strip()
    return frontmatter, body

def extract_email_body(content):
    """Extract email body from markdown content"""
    frontmatter, body = extract_frontmatter(content)
    
    # Look for the draft response section
    if '## Draft Response' in body:
        draft_section = body.split('## Draft Response')[1]
        if '```' in draft_section:
            # Extract content between code blocks
            parts = draft_section.split('```')
            if len(parts) >= 2:
                return parts[1].strip()
    
    # Alternative: look for email draft markers
    lines = body.split('\n')
    in_draft = False
    draft_lines = []
    
    for line in lines:
        if 'Draft Response' in line or '## Email Draft' in line:
            in_draft = True
            continue
        if in_draft:
            if line.startswith('##') and 'Draft' not in line:
                break
            if line.strip() and not line.startswith('**'):
                draft_lines.append(line)
    
    return '\n'.join(draft_lines).strip() if draft_lines else body

def authenticate_gmail(vault_path):
    """Authenticate with Gmail API"""
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    import pickle
    
    SCOPES = [
        'https://www.googleapis.com/auth/gmail.send',
        'https://www.googleapis.com/auth/gmail.compose',
        'https://www.googleapis.com/auth/gmail.readonly'
    ]
    
    token_path = Path(vault_path).parent / 'credentials' / 'token.pickle'
    credentials_path = Path(vault_path).parent / 'credentials' / 'credentials.json'
    
    creds = None
    if token_path.exists():
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
        
        # Check if credentials have the required scopes
        if creds and creds.valid:
            required_scope = 'https://www.googleapis.com/auth/gmail.send'
            if required_scope not in creds.scopes:
                print(f"⚠️  Existing token has insufficient scopes: {creds.scopes}")
                print(f"   Need: {required_scope}")
                print("   Will re-authenticate with correct scopes...")
                creds = None  # Force re-authentication
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not credentials_path.exists():
                raise FileNotFoundError(f"Missing {credentials_path}")
            
            print("\n🌐 Opening browser for Gmail authentication...")
            print("   Please allow Gmail send permissions when prompted.")
            flow = InstalledAppFlow.from_client_secrets_file(
                str(credentials_path), SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save credentials
        if creds and creds.valid:
            token_path.parent.mkdir(parents=True, exist_ok=True)
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)
            print(f"✅ Token saved to: {token_path}")
    
    return creds

def create_message(to, subject, body):
    """Create a Gmail API message"""
    message = MIMEText(body, 'plain', 'utf-8')
    message['to'] = to
    message['from'] = 'me'
    message['subject'] = subject
    
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    return {'raw': raw_message}

def send_email(to, subject, body, creds):
    """Send email via Gmail API"""
    from googleapiclient.discovery import build
    
    service = build('gmail', 'v1', credentials=creds)
    message = create_message(to, subject, body)
    
    sent_message = service.users().messages().send(
        userId='me',
        body=message
    ).execute()
    
    return sent_message

def send_approved_email(approval_file, vault_path):
    """Send an approved email"""
    
    content = approval_file.read_text(encoding='utf-8')
    frontmatter, body = extract_frontmatter(content)
    
    # Extract email details - handle both formats
    to_email = frontmatter.get('to', '')
    subject = frontmatter.get('subject', '')
    original_gmail_id = frontmatter.get('original_gmail_id', '')
    
    # If no 'to' field, extract from the draft response section
    if not to_email:
        # Look for "**To:**" in the body
        to_match = re.search(r'\*\*To:\*\*.*?<([^>]+)>', body)
        if to_match:
            to_email = to_match.group(1)
        
        # If still not found, use the 'from' field (sender of original email)
        if not to_email:
            from_field = frontmatter.get('from', '')
            from_match = re.search(r'<([^>]+)>', from_field)
            if from_match:
                to_email = from_match.group(1)
    
    # Handle subject - add Re: prefix if needed
    if not subject:
        subject = frontmatter.get('subject', 'Re: Email')
    if not subject.startswith('Re:'):
        subject = f"Re: {subject}"
    
    if not to_email:
        print(f"ERROR: Missing recipient email in {approval_file.name}")
        return None
    
    # Extract the draft body from code block after "## Draft Response"
    email_body = ""
    draft_match = re.search(r'## Draft Response.*?```(?:\s*\n)?(.*?)```', body, re.DOTALL)
    if draft_match:
        email_body = draft_match.group(1).strip()
    else:
        # Fallback: extract from any code block
        code_match = re.search(r'```\s*\n(.*?)\n```', body, re.DOTALL)
        if code_match:
            email_body = code_match.group(1).strip()
    
    if not email_body:
        email_body = extract_email_body(content)
    
    # If body still has markdown formatting, clean it up
    if email_body.startswith('**To:**'):
        lines = email_body.split('\n')
        clean_lines = []
        for line in lines:
            if not line.startswith('**'):
                clean_lines.append(line)
        email_body = '\n'.join(clean_lines).strip()
    
    print(f"SENDING EMAIL:")
    print(f"  To: {to_email}")
    print(f"  Subject: {subject}")
    print(f"  Body preview: {email_body[:100]}...")
    
    # Authenticate
    print("\nAuthenticating with Gmail...")
    creds = authenticate_gmail(vault_path)
    
    # Send
    print("Sending email...")
    result = send_email(to_email, subject, email_body, creds)
    
    print(f"✅ Email sent successfully! Gmail ID: {result['id']}")
    
    return result

def move_to_done(approval_file, vault_path, email_result):
    """Move processed approval to Done folder"""
    done_path = Path(vault_path) / 'Done' / approval_file.name
    done_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Add processing timestamp
    content = approval_file.read_text(encoding='utf-8')
    content += f"\n\n---\nSent: {datetime.now().isoformat()}\nGmail ID: {email_result['id']}\nStatus: completed\n"
    
    done_path.write_text(content, encoding='utf-8')
    approval_file.unlink()
    
    print(f"MOVED_TO_DONE: {approval_file.name}")
    return done_path

def log_action(vault_path, approval_file, email_result, frontmatter=None):
    """Log the email sending action"""
    log_dir = Path(vault_path) / 'Logs'
    log_dir.mkdir(parents=True, exist_ok=True)
    
    log_file = log_dir / 'email_actions.json'
    
    import json
    
    # Load existing logs
    actions = []
    if log_file.exists():
        try:
            with open(log_file, 'r') as f:
                actions = json.load(f)
        except:
            actions = []
    
    # Add new action
    if not frontmatter:
        try:
            frontmatter, _ = extract_frontmatter(approval_file.read_text(encoding='utf-8'))
        except:
            frontmatter = {}
    
    action = {
        'timestamp': datetime.now().isoformat(),
        'type': 'email_sent',
        'to': frontmatter.get('to', '') or frontmatter.get('from', ''),
        'subject': frontmatter.get('subject', ''),
        'gmail_id': email_result['id'],
        'original_gmail_id': frontmatter.get('original_gmail_id', '')
    }
    
    actions.append(action)
    
    # Save (keep last 100)
    with open(log_file, 'w') as f:
        json.dump(actions[-100:], f, indent=2)
    
    print(f"LOGGED_ACTION: email_sent to {action['to']}")

def update_dashboard(vault_path, summary):
    """Update dashboard with activity"""
    dashboard_path = Path(vault_path) / 'Dashboard.md'
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    if not dashboard_path.exists():
        return
    
    content = dashboard_path.read_text(encoding='utf-8')
    
    # Update timestamp
    content = re.sub(
        r'last_updated: \d{4}-\d{2}-\d{2}',
        f'last_updated: {datetime.now().strftime("%Y-%m-%d")}',
        content
    )
    
    # Add to recent activity
    activity_line = f"- [{timestamp}] {summary}"
    
    if '## Recent Activity' in content:
        content = content.replace(
            '## Recent Activity\n',
            f'## Recent Activity\n{activity_line}\n'
        )
    
    dashboard_path.write_text(content, encoding='utf-8')
    print("UPDATED_DASHBOARD")

def main():
    if len(sys.argv) < 2:
        print("Usage: python send_approved_email.py <approval_file_path> [vault_path]")
        sys.exit(1)
    
    approval_file = Path(sys.argv[1])
    vault_path = sys.argv[2] if len(sys.argv) > 2 else str(approval_file.parent.parent)
    
    if not approval_file.exists():
        print(f"ERROR: File not found: {approval_file}")
        sys.exit(1)
    
    print(f"PROCESSING APPROVED EMAIL: {approval_file.name}")
    print("="*60)
    
    try:
        # Extract frontmatter before sending (for logging)
        content = approval_file.read_text(encoding='utf-8')
        frontmatter, _ = extract_frontmatter(content)
        
        # Send email
        result = send_approved_email(approval_file, vault_path)

        if result:
            # Move to done
            move_to_done(approval_file, vault_path, result)

            # Log action (pass frontmatter to avoid re-reading moved file)
            log_action(vault_path, approval_file, result, frontmatter)

            # Update dashboard
            update_dashboard(vault_path, "Email sent successfully via Gmail API")

            print("\n" + "="*60)
            print("SUCCESS: Email sent and processed!")
        else:
            print("\nERROR: Failed to send email")
            sys.exit(1)
            
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
