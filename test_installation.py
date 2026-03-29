#!/usr/bin/env python3
"""
Test script to verify Bronze Tier installation and functionality
"""

import sys
from pathlib import Path
import time

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def check_folder_structure():
    """Verify the vault folder structure exists"""
    print_header("Checking Folder Structure")

    vault_path = Path(__file__).parent / 'AI_Employee_Vault'
    required_folders = [
        'Inbox',
        'Needs_Action',
        'Done',
        'Plans',
        'Logs',
        'Pending_Approval',
        'Approved',
        'Rejected'
    ]

    all_exist = True
    for folder in required_folders:
        folder_path = vault_path / folder
        exists = folder_path.exists()
        status = "[OK]" if exists else "[MISSING]"
        print(f"  {status} {folder}/")
        if not exists:
            all_exist = False

    return all_exist

def check_core_files():
    """Verify core files exist"""
    print_header("Checking Core Files")

    vault_path = Path(__file__).parent / 'AI_Employee_Vault'
    required_files = [
        ('Dashboard.md', vault_path / 'Dashboard.md'),
        ('Company_Handbook.md', vault_path / 'Company_Handbook.md'),
        ('base_watcher.py', Path(__file__).parent / 'watchers' / 'base_watcher.py'),
        ('filesystem_watcher.py', Path(__file__).parent / 'watchers' / 'filesystem_watcher.py'),
        ('process-tasks skill', Path(__file__).parent / '.claude' / 'skills' / 'process-tasks.md'),
    ]

    all_exist = True
    for name, file_path in required_files:
        exists = file_path.exists()
        status = "[OK]" if exists else "[MISSING]"
        print(f"  {status} {name}")
        if not exists:
            all_exist = False

    return all_exist

def check_dependencies():
    """Check if required Python packages are installed"""
    print_header("Checking Python Dependencies")

    dependencies = ['watchdog']
    all_installed = True

    for dep in dependencies:
        try:
            __import__(dep)
            print(f"  [OK] {dep}")
        except ImportError:
            print(f"  [MISSING] {dep} - NOT INSTALLED")
            all_installed = False

    return all_installed

def create_test_file():
    """Create a test file in the Inbox"""
    print_header("Creating Test File")

    inbox_path = Path(__file__).parent / 'AI_Employee_Vault' / 'Inbox'
    test_file = inbox_path / 'test_verification.txt'

    try:
        test_file.write_text(f"Test file created at {time.strftime('%Y-%m-%d %H:%M:%S')}\n\nThis file verifies the Bronze Tier installation.")
        print(f"  [OK] Created test file: {test_file.name}")
        print(f"  --> Location: {test_file}")
        return True
    except Exception as e:
        print(f"  [FAIL] Failed to create test file: {e}")
        return False

def check_needs_action():
    """Check if there are tasks in Needs_Action"""
    print_header("Checking Needs_Action Folder")

    needs_action_path = Path(__file__).parent / 'AI_Employee_Vault' / 'Needs_Action'
    files = list(needs_action_path.glob('*.md'))

    if files:
        print(f"  [OK] Found {len(files)} task(s) ready for processing:")
        for f in files[:5]:  # Show first 5
            print(f"    - {f.name}")
        if len(files) > 5:
            print(f"    ... and {len(files) - 5} more")
    else:
        print("  [INFO] No tasks found (this is normal for a fresh installation)")

    return True

def main():
    """Run all verification checks"""
    print("\n" + "#"*60)
    print("  AI EMPLOYEE - BRONZE TIER VERIFICATION")
    print("#"*60)

    results = []

    # Run all checks
    results.append(("Folder Structure", check_folder_structure()))
    results.append(("Core Files", check_core_files()))
    results.append(("Dependencies", check_dependencies()))
    results.append(("Test File Creation", create_test_file()))
    results.append(("Needs Action Check", check_needs_action()))

    # Summary
    print_header("Verification Summary")

    all_passed = all(result[1] for result in results)

    for name, passed in results:
        status = "[PASS]" if passed else "[FAIL]"
        print(f"  {status} - {name}")

    print("\n" + "="*60)

    if all_passed:
        print("  SUCCESS: BRONZE TIER INSTALLATION VERIFIED!")
        print("="*60)
        print("\n  Next Steps:")
        print("  1. Start the watcher: python watchers/filesystem_watcher.py")
        print("  2. Run Claude Code: claude")
        print("  3. Process tasks: /process-tasks")
        print("\n  See QUICKSTART.md for detailed instructions.")
        return 0
    else:
        print("  WARNING: SOME CHECKS FAILED")
        print("="*60)
        print("\n  Please review the errors above and:")
        print("  1. Install missing dependencies: pip install -r requirements.txt")
        print("  2. Verify all files were created correctly")
        print("  3. Run this script again: python test_installation.py")
        return 1

if __name__ == '__main__':
    sys.exit(main())
