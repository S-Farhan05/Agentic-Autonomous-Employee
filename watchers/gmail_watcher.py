#!/usr/bin/env python3
"""
Gmail Watcher - Monitors Gmail inbox for important emails

Silver Tier: This watcher monitors Gmail using the Gmail API and creates
tasks in Needs_Action folder for emails that require attention.
"""

import time
import logging
from pathlib import Path
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle
import os.path

# If modifying these scopes, delete the file token.pickle
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class GmailWatcher:
    """Watcher for Gmail inbox"""

    def __init__(self, vault_path: str, check_interval: int = 120):
        """
        Initialize Gmail watcher

        Args:
            vault_path: Path to the Obsidian vault
            check_interval: Seconds between checks (default: 120)
        """
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.check_interval = check_interval
        self.logger = self._setup_logger()
        self.processed_ids = set()
        self.service = None

        # Ensure directories exist
        self.needs_action.mkdir(parents=True, exist_ok=True)

    def _setup_logger(self):
        """Setup logging for Gmail watcher"""
        logger = logging.getLogger('GmailWatcher')
        logger.setLevel(logging.INFO)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # File handler
        log_dir = self.vault_path / 'Logs'
        log_dir.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(
            log_dir / 'gmail_watcher.log'
        )
        file_handler.setLevel(logging.DEBUG)

        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        return logger

    def authenticate(self):
        """Authenticate with Gmail API"""
        creds = None

        # Token file stores user's access and refresh tokens
        token_path = self.vault_path.parent / 'credentials' / 'token.pickle'
        credentials_path = self.vault_path.parent / 'credentials' / 'credentials.json'

        if token_path.exists():
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)

        # If no valid credentials, let user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not credentials_path.exists():
                    self.logger.error(f"Credentials file not found: {credentials_path}")
                    self.logger.error("Please download credentials.json from Google Cloud Console")
                    raise FileNotFoundError(f"Missing {credentials_path}")

                flow = InstalledAppFlow.from_client_secrets_file(
                    str(credentials_path), SCOPES)
                creds = flow.run_local_server(port=0)

            # Save credentials for next run
            token_path.parent.mkdir(parents=True, exist_ok=True)
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('gmail', 'v1', credentials=creds)
        self.logger.info("Gmail authentication successful")

    def check_for_updates(self):
        """Check Gmail for new important emails"""
        if not self.service:
            self.authenticate()

        try:
            # Query for unread important emails
            results = self.service.users().messages().list(
                userId='me',
                q='is:unread (is:important OR from:client OR subject:invoice OR subject:urgent)',
                maxResults=10
            ).execute()

            messages = results.get('messages', [])

            # Filter out already processed
            new_messages = [
                m for m in messages
                if m['id'] not in self.processed_ids
            ]

            return new_messages

        except Exception as e:
            self.logger.error(f"Error checking Gmail: {e}")
            return []

    def create_action_file(self, message):
        """Create task file for email in Needs_Action folder"""
        try:
            # Get full message details
            msg = self.service.users().messages().get(
                userId='me',
                id=message['id'],
                format='full'
            ).execute()

            # Extract headers
            headers = {
                h['name']: h['value']
                for h in msg['payload']['headers']
            }

            sender = headers.get('From', 'Unknown')
            subject = headers.get('Subject', 'No Subject')
            date = headers.get('Date', '')

            # Extract body (simplified - handles plain text)
            body = self._get_email_body(msg)

            # Determine priority
            priority = 'high' if any(
                keyword in subject.lower()
                for keyword in ['urgent', 'asap', 'important', 'invoice']
            ) else 'medium'

            # Create task file
            content = f'''---
type: email
from: {sender}
subject: {subject}
received: {datetime.now().isoformat()}
priority: {priority}
status: pending
gmail_id: {message['id']}
---

## Email from {sender}

**Subject:** {subject}
**Date:** {date}
**Priority:** {priority}

## Email Content

{body[:500]}{'...' if len(body) > 500 else ''}

## Suggested Actions
- [ ] Read full email
- [ ] Draft response
- [ ] Create approval request if reply needed
- [ ] Move to Done when processed

## Notes
Add any notes or observations here.
'''

            # Create filename
            safe_subject = "".join(
                c for c in subject[:30]
                if c.isalnum() or c in (' ', '-', '_')
            ).strip()
            filename = f'EMAIL_{safe_subject}_{message["id"][:8]}.md'
            filepath = self.needs_action / filename

            filepath.write_text(content, encoding='utf-8')
            self.processed_ids.add(message['id'])

            self.logger.info(f"Created task for email: {subject}")
            return filepath

        except Exception as e:
            self.logger.error(f"Error creating action file: {e}")
            return None

    def _get_email_body(self, msg):
        """Extract email body from message"""
        try:
            if 'parts' in msg['payload']:
                # Multipart message
                for part in msg['payload']['parts']:
                    if part['mimeType'] == 'text/plain':
                        data = part['body'].get('data', '')
                        if data:
                            import base64
                            return base64.urlsafe_b64decode(data).decode('utf-8')
            else:
                # Simple message
                data = msg['payload']['body'].get('data', '')
                if data:
                    import base64
                    return base64.urlsafe_b64decode(data).decode('utf-8')
        except Exception as e:
            self.logger.debug(f"Error extracting body: {e}")

        return "[Email body could not be extracted]"

    def run(self):
        """Main watcher loop"""
        self.logger.info("="*60)
        self.logger.info("GMAIL WATCHER STARTED")
        self.logger.info("="*60)
        self.logger.info(f"Monitoring Gmail inbox")
        self.logger.info(f"Check interval: {self.check_interval} seconds")
        self.logger.info(f"Vault path: {self.vault_path}")
        self.logger.info("="*60)

        # Authenticate on startup
        try:
            self.authenticate()
        except Exception as e:
            self.logger.error(f"Authentication failed: {e}")
            return

        try:
            while True:
                messages = self.check_for_updates()

                if messages:
                    self.logger.info(f"Found {len(messages)} new email(s)")
                    for msg in messages:
                        self.create_action_file(msg)
                else:
                    self.logger.debug("No new emails")

                time.sleep(self.check_interval)

        except KeyboardInterrupt:
            self.logger.info("")
            self.logger.info("="*60)
            self.logger.info("Gmail watcher stopped by user")
            self.logger.info("="*60)


if __name__ == '__main__':
    import sys

    # Get vault path from command line or use default
    if len(sys.argv) > 1:
        vault_path = sys.argv[1]
    else:
        vault_path = Path(__file__).parent.parent / 'AI_Employee_Vault'

    # Optional: specify check interval
    check_interval = int(sys.argv[2]) if len(sys.argv) > 2 else 120

    watcher = GmailWatcher(str(vault_path), check_interval)
    watcher.run()
