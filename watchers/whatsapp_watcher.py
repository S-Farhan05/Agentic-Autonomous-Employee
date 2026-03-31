#!/usr/bin/env python3
"""
WhatsApp Watcher - Monitors WhatsApp Web for important messages

Silver Tier: This watcher monitors WhatsApp using Playwright automation
and creates tasks for messages that require attention.

Note: This uses WhatsApp Web automation. Be aware of WhatsApp's terms of service.
"""

import time
import logging
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

class WhatsAppWatcher:
    """Watcher for WhatsApp messages"""

    def __init__(self, vault_path: str, session_path: str, check_interval: int = 60):
        """
        Initialize WhatsApp watcher

        Args:
            vault_path: Path to the Obsidian vault
            session_path: Path to store WhatsApp session data
            check_interval: Seconds between checks (default: 60)
        """
        self.vault_path = Path(vault_path)
        self.session_path = Path(session_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.check_interval = check_interval
        self.logger = self._setup_logger()
        self.processed_messages = set()

        # Keywords that trigger task creation
        self.keywords = [
            'urgent', 'asap', 'invoice', 'payment', 'help',
            'quote', 'pricing', 'project', 'deadline', 'meeting'
        ]

        # Ensure directories exist
        self.needs_action.mkdir(parents=True, exist_ok=True)
        self.session_path.mkdir(parents=True, exist_ok=True)

    def _setup_logger(self):
        """Setup logging for WhatsApp watcher"""
        logger = logging.getLogger('WhatsAppWatcher')
        logger.setLevel(logging.INFO)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # File handler
        log_dir = self.vault_path / 'Logs'
        log_dir.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(
            log_dir / 'whatsapp_watcher.log'
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

    def check_for_updates(self):
        """Check WhatsApp for new important messages"""
        messages = []

        try:
            with sync_playwright() as p:
                # Launch browser with persistent context (saves login)
                browser = p.chromium.launch_persistent_context(
                    str(self.session_path),
                    headless=False,  # Set to True for background operation
                    args=['--no-sandbox']
                )

                page = browser.pages[0] if browser.pages else browser.new_page()
                page.goto('https://web.whatsapp.com', timeout=60000)

                # Wait for WhatsApp to load
                try:
                    page.wait_for_selector('[data-testid="chat-list"]', timeout=30000)
                except PlaywrightTimeout:
                    self.logger.warning("WhatsApp not loaded. May need to scan QR code.")
                    browser.close()
                    return []

                # Find unread chats
                unread_chats = page.query_selector_all('[aria-label*="unread"]')

                for chat in unread_chats[:5]:  # Process max 5 at a time
                    try:
                        # Click on chat to open
                        chat.click()
                        time.sleep(1)

                        # Get chat name
                        chat_name_elem = page.query_selector('[data-testid="conversation-header"]')
                        chat_name = chat_name_elem.inner_text() if chat_name_elem else "Unknown"

                        # Get messages
                        message_elems = page.query_selector_all('[data-testid="msg-container"]')

                        # Get last few messages
                        for msg_elem in message_elems[-3:]:
                            text = msg_elem.inner_text().lower()

                            # Check if contains keywords
                            if any(keyword in text for keyword in self.keywords):
                                # Create unique ID
                                msg_id = f"{chat_name}_{hash(text)}"

                                if msg_id not in self.processed_messages:
                                    messages.append({
                                        'chat': chat_name,
                                        'text': msg_elem.inner_text(),
                                        'id': msg_id
                                    })
                                    self.processed_messages.add(msg_id)

                    except Exception as e:
                        self.logger.debug(f"Error processing chat: {e}")
                        continue

                browser.close()

        except Exception as e:
            self.logger.error(f"Error checking WhatsApp: {e}")

        return messages

    def create_action_file(self, message):
        """Create task file for WhatsApp message"""
        try:
            chat_name = message['chat']
            text = message['text']
            msg_id = message['id']

            # Determine priority
            priority = 'high' if any(
                keyword in text.lower()
                for keyword in ['urgent', 'asap', 'emergency']
            ) else 'medium'

            # Create task file
            content = f'''---
type: whatsapp
from: {chat_name}
received: {datetime.now().isoformat()}
priority: {priority}
status: pending
message_id: {msg_id}
---

## WhatsApp Message from {chat_name}

**Priority:** {priority}
**Received:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Message Content

{text}

## Suggested Actions
- [ ] Read full conversation context
- [ ] Draft response
- [ ] Create approval request if reply needed
- [ ] Move to Done when processed

## Notes
Add any notes or observations here.
'''

            # Create filename
            safe_name = "".join(
                c for c in chat_name[:30]
                if c.isalnum() or c in (' ', '-', '_')
            ).strip()
            filename = f'WHATSAPP_{safe_name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
            filepath = self.needs_action / filename

            filepath.write_text(content, encoding='utf-8')

            self.logger.info(f"Created task for WhatsApp message from: {chat_name}")
            return filepath

        except Exception as e:
            self.logger.error(f"Error creating action file: {e}")
            return None

    def run(self):
        """Main watcher loop"""
        self.logger.info("="*60)
        self.logger.info("WHATSAPP WATCHER STARTED")
        self.logger.info("="*60)
        self.logger.info(f"Monitoring WhatsApp Web")
        self.logger.info(f"Check interval: {self.check_interval} seconds")
        self.logger.info(f"Vault path: {self.vault_path}")
        self.logger.info(f"Session path: {self.session_path}")
        self.logger.info("")
        self.logger.info("IMPORTANT: First run will require QR code scan")
        self.logger.info("Keep browser window open for QR code scanning")
        self.logger.info("="*60)

        try:
            while True:
                messages = self.check_for_updates()

                if messages:
                    self.logger.info(f"Found {len(messages)} important message(s)")
                    for msg in messages:
                        self.create_action_file(msg)
                else:
                    self.logger.debug("No new important messages")

                time.sleep(self.check_interval)

        except KeyboardInterrupt:
            self.logger.info("")
            self.logger.info("="*60)
            self.logger.info("WhatsApp watcher stopped by user")
            self.logger.info("="*60)


if __name__ == '__main__':
    import sys

    # Get vault path from command line or use default
    if len(sys.argv) > 1:
        vault_path = sys.argv[1]
    else:
        vault_path = Path(__file__).parent.parent / 'AI_Employee_Vault'

    # Session path for WhatsApp login persistence
    if len(sys.argv) > 2:
        session_path = sys.argv[2]
    else:
        session_path = Path(__file__).parent.parent / 'whatsapp_session'

    # Optional: specify check interval
    check_interval = int(sys.argv[3]) if len(sys.argv) > 3 else 60

    watcher = WhatsAppWatcher(str(vault_path), str(session_path), check_interval)
    watcher.run()
