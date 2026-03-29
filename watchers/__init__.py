# Watchers Package
# Base classes and utilities for AI Employee watchers

from .base_watcher import BaseWatcher
from .filesystem_watcher import FileSystemWatcher, DropFolderHandler

__all__ = ['BaseWatcher', 'FileSystemWatcher', 'DropFolderHandler']
__version__ = '1.0.0'
