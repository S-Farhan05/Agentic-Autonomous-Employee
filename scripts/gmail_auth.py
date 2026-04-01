"""
Gmail Authentication Helper
Run this to authenticate Gmail API credentials
"""

import os
import sys
from pathlib import Path

# Check if credentials file exists
credentials_path = Path('credentials/credentials.json')
token_path = Path('credentials/token.pickle')

print("="*60)
print("GMAIL AUTHENTICATION HELPER")
print("="*60)

if not credentials_path.exists():
    print("\n❌ ERROR: credentials.json not found!")
    print(f"   Expected at: {credentials_path}")
    print("\n   Please download credentials.json from Google Cloud Console:")
    print("   1. Go to https://console.cloud.google.com")
    print("   2. Create/select project")
    print("   3. Enable Gmail API")
    print("   4. Create OAuth 2.0 credentials (Desktop app)")
    print("   5. Download and save as credentials/credentials.json")
    sys.exit(1)

print("\n✅ credentials.json found")

# Check if already authenticated
if token_path.exists():
    print("✅ Already authenticated (token.pickle exists)")
    print("\n   To re-authenticate, delete:")
    print(f"   {token_path}")
    proceed = input("\n   Continue anyway? (y/n): ")
    if proceed.lower() != 'y':
        sys.exit(0)
else:
    print("⏳ Not authenticated yet (token.pickle not found)")

print("\n" + "="*60)
print("AUTHENTICATION STEPS:")
print("="*60)
print("""
1. A browser window will open automatically
2. Select your Google/Gmail account
3. Review permissions (Gmail read access)
4. Click "Allow" or "Continue"
5. Browser will show "Authentication successful" or similar
6. Browser may close automatically or show redirect error (this is OK!)
7. Come back to this terminal - it should say "Authentication successful"

NOTE: If browser shows error after allowing (like redirect_uri_mismatch or 
      400 error), that's OK! The authentication still worked. Just check 
      if token.pickle was created in credentials/ folder.
""")

input("\nPress Enter to start authentication...")

try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    import pickle
    
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    
    print("\n🔐 Starting authentication...")
    
    creds = None
    if token_path.exists():
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
            print("✅ Loaded existing token")
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Refreshing expired token...")
            creds.refresh(Request())
        else:
            print("🌐 Opening browser for authentication...")
            flow = InstalledAppFlow.from_client_secrets_file(
                str(credentials_path), SCOPES)
            
            # Try different methods
            try:
                # Method 1: Default (opens browser)
                creds = flow.run_local_server(port=0)
            except Exception as e1:
                print(f"Method 1 failed: {e1}")
                try:
                    # Method 2: Specific port
                    print("Trying method 2 (port 8080)...")
                    creds = flow.run_local_server(port=8080, open_browser=True)
                except Exception as e2:
                    print(f"Method 2 failed: {e2}")
                    # Method 3: Console flow
                    print("Trying method 3 (console)...")
                    creds = flow.run_console()
        
        # Save credentials
        if creds and creds.valid:
            print("\n✅ Authentication successful!")
            token_path.parent.mkdir(parents=True, exist_ok=True)
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)
            print(f"✅ Token saved to: {token_path}")
            
            # Test the credentials
            print("\n🧪 Testing credentials...")
            from googleapiclient.discovery import build
            service = build('gmail', 'v1', credentials=creds)
            results = service.users().messages().list(userId='me', maxResults=1).execute()
            messages = results.get('messages', [])
            print(f"✅ Gmail API connection successful!")
            print(f"   Found {len(messages)} message(s) in inbox")
            
            print("\n" + "="*60)
            print("AUTHENTICATION COMPLETE!")
            print("="*60)
            print("\nYou can now run:")
            print("  python watchers/gmail_watcher.py")
        else:
            print("\n❌ Authentication failed - credentials not valid")
            sys.exit(1)
    else:
        print("\n✅ Token already valid, no re-authentication needed")
        
except ImportError as e:
    print(f"\n❌ Missing required packages: {e}")
    print("\nInstall with:")
    print("  pip install google-auth google-auth-oauthlib google-api-python-client")
    sys.exit(1)
except Exception as e:
    print(f"\n❌ Authentication error: {e}")
    print("\nTroubleshooting:")
    print("1. Make sure credentials.json is valid")
    print("2. Check OAuth consent screen is configured in Google Cloud")
    print("3. Make sure Gmail API is enabled")
    print("4. Try deleting token.pickle and retry")
    sys.exit(1)
