# ⚡ QUICK START - COPY-PASTE THESE COMMANDS

## For Windows (Command Prompt or PowerShell)

# Step 1: Create folder and navigate
mkdir event_pass_system
cd event_pass_system

# Step 2: Download files
# (Download all files from Claude into this folder)

# Step 3: Install packages
pip install flask flask-sqlalchemy pycryptodome pyotp qrcode pillow --break-system-packages

# Step 4: Run application
python app.py

---

## For Mac/Linux (Terminal)

# Step 1: Create folder and navigate
mkdir event_pass_system
cd event_pass_system

# Step 2: Download files
# (Download all files from Claude into this folder)

# Step 3: Install packages
pip3 install flask flask-sqlalchemy pycryptodome pyotp qrcode pillow --break-system-packages

# Step 4: Run application
python3 app.py

---

## Alternative: Using requirements.txt

# Step 1: Navigate to project folder
cd event_pass_system

# Step 2: Install from requirements.txt
pip install -r requirements.txt --break-system-packages

# Step 3: Run
python app.py

---

## After Running

1. Open browser: http://127.0.0.1:5000
2. Register with role "Organizer"
3. Scan QR code with Google Authenticator app
4. Login with username, password, and OTP
5. Create an event
6. Open incognito window, register as "Attendee"
7. Generate pass for the event
8. Go back to organizer account
9. Validate the pass

---

## Test Users for Quick Demo

### User 1 (Organizer):
- Username: organizer1
- Email: org@example.com
- Password: SecurePass123
- Role: Organizer

### User 2 (Attendee):
- Username: attendee1  
- Email: att@example.com
- Password: SecurePass456
- Role: Attendee

### User 3 (Admin - if needed):
- Username: admin1
- Email: admin@example.com
- Password: AdminPass789
- Role: Admin (change in code to allow this)

---

## Google Authenticator Setup

1. Download app:
   - Android: https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2
   - iPhone: https://apps.apple.com/app/google-authenticator/id388497605

2. Open app after registration
3. Tap "+" or "Scan QR code"
4. Scan the QR code shown on screen
5. Use the 6-digit code when logging in

---

## If Google Authenticator Not Available

Use these alternatives:
- Authy (iOS/Android)
- Microsoft Authenticator
- 2FAS Auth

OR use manual entry:
- Copy the secret key shown below QR code
- In authenticator app, choose "Manual entry"
- Paste the secret key

---

## Common Issues & Fixes

### "pip not recognized"
Try: python -m pip install ...

### "Permission denied"
Windows: Run as Administrator
Mac/Linux: Use sudo (not recommended) or --user flag

### "Port 5000 already in use"
Edit app.py, last line:
app.run(debug=True, port=5001)

### "Module pycryptodome not found"
pip uninstall pycrypto
pip install pycryptodome --break-system-packages

---

## Files You Need

Make sure you have downloaded these files:

MUST HAVE:
- app.py (main application)
- templates/ folder with ALL 10 HTML files

HELPFUL:
- requirements.txt
- README.md
- VIVA_CHEAT_SHEET.md
- SETUP_GUIDE.md

---

## Pre-Evaluation Checklist

Run through this:

[ ] Python installed (python --version shows 3.8+)
[ ] All packages installed (no errors when running pip install)
[ ] Application starts (shows "Running on http://127.0.0.1:5000")
[ ] Homepage loads in browser
[ ] Can register a user
[ ] QR code appears
[ ] Google Authenticator app on phone
[ ] Can scan QR and get OTP codes
[ ] Can login with OTP
[ ] Can create event
[ ] Can generate pass
[ ] Can validate pass

If ALL checked, you're 100% ready! ✅

---

## During Evaluation

Keep these open:
1. Terminal running the app
2. Browser at http://127.0.0.1:5000
3. Google Authenticator on phone
4. VIVA_CHEAT_SHEET.md file
5. app.py in a text editor (to show code if asked)

---

## Emergency Backup Plan

If something breaks during demo:

1. Have screenshots ready of:
   - Homepage with security features
   - Registration page
   - 2FA QR code
   - Dashboard
   - Event creation
   - Pass with QR code
   - Validation page

2. Have code snippets ready to show:
   - Password hashing function
   - Encryption function
   - Digital signature function

3. Can explain everything even without running demo

---

## Contact

If you need help:
- Read README.md first
- Check VIVA_CHEAT_SHEET.md for answers
- Review SETUP_GUIDE.md for detailed steps

---

EVERYTHING IS READY! 
Just download, install, run, and you're good to go!

Good luck! 🚀
