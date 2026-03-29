# filesystem_watcher.py - Monitor a drop folder for new files
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil
import time
import logging
from datetime import datetime

class DropFolderHandler(FileSystemEventHandler):
    """Handler for file system events in the drop folder"""

    def __init__(self, vault_path: str):
        """
        Initialize the drop folder handler

        Args:
            vault_path: Path to the Obsidian vault
        """
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.inbox = self.vault_path / 'Inbox'

        # Ensure directories exist
        self.needs_action.mkdir(parents=True, exist_ok=True)
        self.inbox.mkdir(parents=True, exist_ok=True)

        # Setup logging
        self.logger = self._setup_logger()

    def _setup_logger(self):
        """Setup logging for this handler"""
        logger = logging.getLogger('DropFolderHandler')
        logger.setLevel(logging.INFO)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # File handler
        log_dir = self.vault_path / 'Logs'
        log_dir.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(
            log_dir / 'filesystem_watcher.log'
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

    def on_created(self, event):
        """
        Called when a file or directory is created

        Args:
            event: File system event
        """
        if event.is_directory:
            return

        source = Path(event.src_path)

        # Ignore temporary files and hidden files
        if source.name.startswith('.') or source.name.startswith('~'):
            return

        try:
            # Wait a moment to ensure file is fully written
            time.sleep(0.5)

            # Copy file to Needs_Action with prefix
            dest = self.needs_action / f'FILE_{source.name}'
            shutil.copy2(source, dest)

            # Create metadata file
            self.create_metadata(source, dest)

            self.logger.info(f'Processed new file: {source.name}')

        except Exception as e:
            self.logger.error(f'Error processing file {source.name}: {e}')

    def create_metadata(self, source: Path, dest: Path):
        """
        Create a markdown metadata file for the dropped file

        Args:
            source: Original file path
            dest: Destination file path in Needs_Action
        """
        meta_path = dest.with_suffix('.md')

        # Get file stats
        stats = source.stat()
        size_kb = stats.st_size / 1024

        content = f'''---
type: file_drop
original_name: {source.name}
size: {size_kb:.2f} KB
received: {datetime.now().isoformat()}
priority: medium
status: pending
---

## New File Dropped for Processing

**File**: {dest.name}
**Original Location**: {source}
**Size**: {size_kb:.2f} KB
**Received**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Suggested Actions
- [ ] Review file contents
- [ ] Determine appropriate action
- [ ] Process or forward as needed
- [ ] Move to /Done when complete

## Notes
Add any notes or observations here.
'''

        meta_path.write_text(content, encoding='utf-8')


class FileSystemWatcher:
    """Main watcher class for monitoring the drop folder"""

    def __init__(self, vault_path: str, watch_folder: str = None):
        """
        Initialize the file system watcher

        Args:
            vault_path: Path to the Obsidian vault
            watch_folder: Folder to watch (defaults to vault/Inbox)
        """
        self.vault_path = Path(vault_path)
        self.watch_folder = Path(watch_folder) if watch_folder else self.vault_path / 'Inbox'

        # Ensure watch folder exists
        self.watch_folder.mkdir(parents=True, exist_ok=True)

        # Setup logging
        self.logger = logging.getLogger('FileSystemWatcher')
        self.logger.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # Create event handler and observer
        self.event_handler = DropFolderHandler(str(self.vault_path))
        self.observer = Observer()

    def run(self):
        """Start watching the folder"""
        self.logger.info(f'Starting FileSystemWatcher')
        self.logger.info(f'Watching folder: {self.watch_folder}')
        self.logger.info(f'Vault path: {self.vault_path}')

        self.observer.schedule(
            self.event_handler,
            str(self.watch_folder),
            recursive=False
        )
        self.observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.info('Watcher stopped by user')
            self.observer.stop()

        self.observer.join()


if __name__ == '__main__':
    import sys

    # Get vault path from command line or use default
    if len(sys.argv) > 1:
        vault_path = sys.argv[1]
    else:
        vault_path = Path(__file__).parent.parent / 'AI_Employee_Vault'

    # Optional: specify custom watch folder
    watch_folder = sys.argv[2] if len(sys.argv) > 2 else None

    watcher = FileSystemWatcher(str(vault_path), watch_folder)
    watcher.run()
