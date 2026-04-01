"""
Simple Gmail Auth Test - Just check if we can authenticate
"""
import sys
from pathlib import Path

credentials_path = Path('credentials/credentials.json')

print("="*60)
print("GMAIL API QUICK AUTH TEST")
print("="*60)

# Step 1: Check credentials file
print("\n[1/5] Checking credentials.json...")
if not credentials_path.exists():
    print("❌ credentials.json NOT found!")
    sys.exit(1)
print("✅ credentials.json found")

# Step 2: Import required libraries
print("\n[2/5] Checking required libraries...")
try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    import pickle
    print("✅ All libraries available")
except ImportError as e:
    print(f"❌ Missing library: {e}")
    print("\nRun: pip install google-auth google-auth-oauthlib google-api-python-client")
    sys.exit(1)

# Step 3: Check if already authenticated
print("\n[3/5] Checking existing authentication...")
token_path = Path('credentials/token.pickle')
if token_path.exists():
    print("✅ Already authenticated (token.pickle exists)")
    print("   We can proceed with Gmail watcher!")
    sys.exit(0)
else:
    print("⏳ Not authenticated yet (need to create token.pickle)")

# Step 4: Start authentication
print("\n[4/5] Starting authentication...")
print("    Browser will open in 3 seconds...")

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

import time
time.sleep(3)

try:
    flow = InstalledAppFlow.from_client_secrets_file(
        str(credentials_path), SCOPES)
    
    print("\n🌐 Opening browser...")
    print("    If browser doesn't open, go to the URL shown below")
    
    # Open browser on port 8080
    creds = flow.run_local_server(
        port=8080,
        open_browser=True,
        authorization_prompt_message='Opening browser to: {url}',
        success_message='Authentication successful! You can close this window.',
        redirect_uri_trailing_slash=False
    )
    
    # Step 5: Save token
    print("\n[5/5] Saving authentication token...")
    with open(token_path, 'wb') as token:
        pickle.dump(creds, token)
    
    print("✅ Token saved to: credentials/token.pickle")
    print("\n" + "="*60)
    print("SUCCESS! Gmail authentication complete!")
    print("="*60)
    print("\nNext step: Run the Gmail watcher")
    print("  python watchers/gmail_watcher.py")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nCommon issues:")
    print("1. OAuth consent screen not configured")
    print("2. Gmail API not enabled")
    print("3. Wrong redirect URI")
    print("\nTry this:")
    print("1. Go to https://console.cloud.google.com")
    print("2. Select project: ai-employee1-491909")
    print("3. Go to 'APIs & Services' > 'OAuth consent screen'")
    print("4. Make sure it's configured (External user type is OK)")
    print("5. Go to 'Credentials' and verify OAuth 2.0 Client ID")
    print("6. Make sure Gmail API is enabled")
