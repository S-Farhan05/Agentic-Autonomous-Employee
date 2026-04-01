# Gmail OAuth2 Setup - Fix 400 Error

**Problem:** Browser shows "400. That's an error" when trying to authenticate

**Root Cause:** OAuth consent screen not configured in Google Cloud Console

---

## ✅ Step-by-Step Fix

### **Step 1: Go to Google Cloud Console**

Open: https://console.cloud.google.com

Select your project: **ai-employee1-491909**

---

### **Step 2: Configure OAuth Consent Screen**

1. **Navigate to:** APIs & Services → OAuth consent screen
   
2. **Choose User Type:**
   - Select: **External** (unless you have Google Workspace)
   - Click: **Create**

3. **Fill in App Information:**
   ```
   App name: AI Employee
   User support email: your-email@gmail.com
   App logo: (optional)
   ```

4. **App Domain:**
   ```
   Application home page: (leave blank or put your website)
   Authorized domains: (leave blank for testing)
   ```

5. **Contact Information:**
   ```
   Developer contact email: your-email@gmail.com
   ```

6. **Click: Save and Continue**

---

### **Step 3: Scopes (Important!)**

1. **Click: Add or Remove Scopes**

2. **Add these scopes:**
   ```
   ✓ https://www.googleapis.com/auth/gmail.readonly
   ✓ https://www.googleapis.com/auth/gmail.send
   ✓ https://www.googleapis.com/auth/gmail.compose
   ```

3. **Click: Update → Save and Continue**

---

### **Step 4: Test Users**

1. **Click: Add Users**

2. **Add your Gmail address:**
   ```
   your-email@gmail.com
   ```

3. **Click: Add → Save and Continue**

---

### **Step 5: Enable Gmail API**

1. **Navigate to:** APIs & Services → Library

2. **Search for:** "Gmail API"

3. **Click: Gmail API → Enable**

---

### **Step 6: Verify Credentials**

1. **Navigate to:** APIs & Services → Credentials

2. **Find your OAuth 2.0 Client ID:**
   - Should be type: **Desktop app**
   - Should have redirect URIs configured

3. **If credentials.json is old, create new one:**
   - Click: **Create Credentials** → **OAuth Client ID**
   - Application type: **Desktop app**
   - Download the JSON file
   - Replace `credentials/credentials.json`

---

### **Step 7: Run Authentication Again**

```bash
python scripts/test_gmail_auth.py
```

**What should happen:**

1. Browser opens automatically
2. Google sign-in page appears
3. Select your Gmail account
4. **Warning screen appears:** "Google hasn't verified this app"
   - This is NORMAL for personal projects!
5. **Click: Advanced → Go to AI Employee (unsafe)**
6. **Click: Allow** (grant Gmail permissions)
7. Browser shows: "Authentication successful!"
8. Token saved to: `credentials/token.pickle`

---

## 🎯 What to Click When You See Warning

When browser shows:

```
⚠️ Google hasn't verified this app

AI Employee is requesting access to your Google Account...
```

**DO THIS:**

1. Click: **Advanced** (small link)
2. Click: **Go to AI Employee (unsafe)**
3. Click: **Allow**

**This is normal for development/testing!**

---

## ✅ Verify Authentication Worked

After authentication, check:

```bash
dir credentials\token.pickle
```

Should show:
```
token.pickle file exists (about 1-2 KB)
```

---

## 🧪 Test Gmail Connection

Once token.pickle exists, test the connection:

```bash
python scripts/test_gmail_connection.py
```

Should show:
```
✅ Gmail API connected!
✅ Found X emails in your inbox
```

---

## Common Issues

### **Issue: "redirect_uri_mismatch"**

**Fix:** Make sure credentials.json has these redirect_uris:
```json
"redirect_uris": [
  "http://localhost",
  "http://localhost:8080",
  "http://127.0.0.1:8080"
]
```

### **Issue: "Access blocked"**

**Fix:** Your app is in testing mode. Add your email as test user (Step 4 above).

### **Issue: Browser doesn't open**

**Fix:** 
1. Check pop-up blocker
2. Manually open browser and go to URL shown in terminal
3. Or use `--no-browser` flag and copy/paste URL

### **Issue: Still getting 400 error**

**Try this:**

1. Delete old token (if exists):
   ```bash
   del credentials\token.pickle
   ```

2. Create NEW credentials in Google Cloud:
   - Delete old OAuth client
   - Create new Desktop app OAuth client
   - Download new credentials.json
   - Replace credentials/credentials.json

3. Try authentication again

---

## Quick Test Command

After fixing everything, run:

```bash
python scripts/test_gmail_auth.py
```

Expected flow:
1. ✅ credentials.json found
2. ✅ Libraries available
3. ⏳ Not authenticated yet
4. 🌐 Browser opens
5. You log in and allow
6. ✅ Token saved
7. ✅ SUCCESS message

Then you can run the watcher:
```bash
python watchers/gmail_watcher.py
```

---

## Need Help?

If still stuck, share:
1. Screenshot of the error
2. Your OAuth consent screen status (published or testing)
3. Whether Gmail API is enabled
4. Contents of credentials.json (hide client_secret)
