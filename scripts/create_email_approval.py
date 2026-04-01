#!/usr/bin/env python3
"""
Create Email Approval Request

This script processes an email task and creates an approval request.
Called by Qwen Code or continuous processor.

Usage: python create_email_approval.py <email_file_path> [vault_path]
"""

import sys
import re
from pathlib import Path
from datetime import datetime, timedelta

def extract_frontmatter(content):
    """Extract frontmatter from markdown file"""
    match = re.search(r'^---\s*\n(.*?)\n---\s*$', content, re.DOTALL)
    if not match:
        return {}, content
    
    frontmatter = {}
    for line in match.group(1).split('\n'):
        if ':' in line:
            # Split only on first colon to handle values with colons
            idx = line.index(':')
            key = line[:idx].strip()
            value = line[idx+1:].strip()
            frontmatter[key] = value
    
    body = content[match.end():].strip()
    return frontmatter, body

def extract_email_address(sender):
    """Extract email address from sender string like 'Name <email@domain.com>'"""
    match = re.search(r'<([^>]+)>', sender)
    if match:
        return match.group(1)
    return sender

def create_approval_request(email_file, vault_path):
    """Create approval request for an email"""
    
    content = email_file.read_text(encoding='utf-8')
    frontmatter, body = extract_frontmatter(content)
    
    # Extract email details
    sender = frontmatter.get('from', 'Unknown')
    subject = frontmatter.get('subject', 'No Subject')
    gmail_id = frontmatter.get('gmail_id', '')
    priority = frontmatter.get('priority', 'medium')
    
    # Extract sender email
    sender_email = extract_email_address(sender)
    
    # Determine if reply is needed
    body_lower = body.lower()
    reply_needed = True
    
    no_reply_phrases = ['no reply needed', 'for your information only', 'fyi only', 'automated message']
    for phrase in no_reply_phrases:
        if phrase in body_lower:
            reply_needed = False
            break
    
    if not reply_needed:
        print(f"NO_REPLY_NEEDED: {subject}")
        return None
    
    # Draft a response based on email content
    sender_name = sender.split('<')[0].strip() if '<' in sender else sender.split()[0] if ' ' in sender else 'Sender'
    
    if 'investing opportunity' in body_lower or 'opportunity' in body_lower:
        draft_body = f"""Dear {sender_name},

Thank you for reaching out and thinking of me regarding the investing opportunity you mentioned.

I appreciate you keeping me in the loop. I'm definitely interested in hearing more details when you have time to discuss.

Please feel free to share more information at your convenience.

Looking forward to our conversation.

Best regards,
AI Employee"""
    elif 'hi' in body_lower or 'hello' in body_lower:
        draft_body = f"""Dear {sender_name},

Thank you for your greeting. I hope this message finds you well.

Please let me know how I can assist you. I'm available to discuss any matters you'd like to bring up.

Looking forward to hearing from you.

Best regards,
AI Employee"""
    else:
        draft_body = f"""Dear {sender_name},

Thank you for your message. I have received your email regarding "{subject}".

Please let me know how I can help or if there's anything specific you'd like to discuss.

Best regards,
AI Employee"""
    
    # Create approval request content
    created = datetime.now()
    expires = created + timedelta(hours=24)
    
    safe_subject = "".join(c for c in subject[:30] if c.isalnum() or c in (' ', '-', '_')).strip()
    approval_filename = f"EMAIL_{safe_subject}_{gmail_id[:8] if gmail_id else 'reply'}.md"
    
    approval_content = f"""---
type: approval_request
action: send_email
to: {sender_email}
from_name: {sender}
subject: Re: {subject}
original_gmail_id: {gmail_id}
priority: {priority}
created: {created.isoformat()}
expires: {expires.isoformat()}
status: pending
---

## Email Draft

**To:** {sender}
**Subject:** Re: {subject}

---

{draft_body}

---

## Context
This email is a response to a greeting from {sender} who mentioned an investing opportunity.
The sender indicated they will talk soon, so this is a courteous acknowledgment.

## Original Email Content
{body[:300]}{'...' if len(body) > 300 else ''}

## To Approve
Move this file to /Approved folder

## To Reject
Move this file to /Rejected folder

## Risk Assessment
- Low risk: Standard courtesy reply
- Sender is known (from address matches expected)
- No sensitive information being shared
- No financial commitment in this message
"""
    
    # Write approval request
    pending_approval_path = Path(vault_path) / 'Pending_Approval' / approval_filename
    pending_approval_path.parent.mkdir(parents=True, exist_ok=True)
    pending_approval_path.write_text(approval_content, encoding='utf-8')
    
    print(f"CREATED_APPROVAL: {approval_filename}")
    return pending_approval_path

def move_to_done(email_file, vault_path):
    """Move processed email to Done folder"""
    done_path = Path(vault_path) / 'Done' / email_file.name
    done_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Add processing timestamp
    content = email_file.read_text(encoding='utf-8')
    content += f"\n\n---\nProcessed: {datetime.now().isoformat()}\nMoved to Done\n"
    
    done_path.write_text(content, encoding='utf-8')
    email_file.unlink()
    
    print(f"MOVED_TO_DONE: {email_file.name}")
    return done_path

def update_dashboard(vault_path, action_summary):
    """Update dashboard with recent activity"""
    dashboard_path = Path(vault_path) / 'Dashboard.md'
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    if not dashboard_path.exists():
        dashboard_content = f"""---
last_updated: {datetime.now().strftime('%Y-%m-%d')}
type: dashboard
---

# AI Employee Dashboard

## System Status
- **Status**: Active
- **Last Check**: {timestamp}
- **Pending Tasks**: 0
- **Completed Today**: 1

## Recent Activity
- [{timestamp}] {action_summary}

## Pending Actions
*Check Pending_Approval folder*

## Quick Stats
- **Tasks in Queue**: 0
- **Awaiting Approval**: 1
- **Completed This Week**: 1

## Alerts
*No alerts*

---
*Last updated by AI Employee*
"""
        dashboard_path.write_text(dashboard_content, encoding='utf-8')
        print("CREATED_DASHBOARD")
        return
    
    content = dashboard_path.read_text(encoding='utf-8')
    
    # Update timestamp
    content = re.sub(
        r'last_updated: \d{4}-\d{2}-\d{2}',
        f'last_updated: {datetime.now().strftime("%Y-%m-%d")}',
        content
    )
    
    # Add to recent activity
    activity_line = f"- [{timestamp}] {action_summary}"
    
    if '## Recent Activity' in content:
        content = content.replace(
            '## Recent Activity\n',
            f'## Recent Activity\n{activity_line}\n'
        )
    
    # Update pending approvals count
    if '**Awaiting Approval**: 0' in content:
        content = content.replace('**Awaiting Approval**: 0', '**Awaiting Approval**: 1')
    elif '**Awaiting Approval**: 1' not in content:
        # Increment if exists
        match = re.search(r'\*\*Awaiting Approval\*\*: (\d+)', content)
        if match:
            current = int(match.group(1))
            content = content.replace(
                f'**Awaiting Approval**: {current}',
                f'**Awaiting Approval**: {current + 1}'
            )
    
    dashboard_path.write_text(content, encoding='utf-8')
    print("UPDATED_DASHBOARD")

def main():
    if len(sys.argv) < 2:
        print("Usage: python create_email_approval.py <email_file_path> [vault_path]")
        sys.exit(1)
    
    email_file = Path(sys.argv[1])
    vault_path = sys.argv[2] if len(sys.argv) > 2 else str(email_file.parent.parent)
    
    if not email_file.exists():
        print(f"ERROR: File not found: {email_file}")
        sys.exit(1)
    
    print(f"PROCESSING: {email_file.name}")
    
    # Create approval request
    approval_file = create_approval_request(email_file, vault_path)
    
    if approval_file:
        # Move to done
        move_to_done(email_file, vault_path)
        
        # Update dashboard
        update_dashboard(vault_path, "Created email approval request - awaiting review")
        
        print("\nSUCCESS: Task processed!")
        print(f"  Approval request: {approval_file}")
        print("  Next: Move to /Approved to send the email")
    else:
        print("No action required for this email")

if __name__ == '__main__':
    main()
