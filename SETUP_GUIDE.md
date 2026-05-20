# 🚀 SETUP GUIDE - DO THIS BEFORE EVAL TOMORROW

## ⏰ TIME REQUIRED: 10 minutes

---

## STEP 1: Download All Files (2 mins)

Download these files to a folder on your computer:
```
event_pass_system/
├── app.py
├── requirements.txt
├── README.md
├── VIVA_CHEAT_SHEET.md
└── templates/
    └── [all HTML files]
```

**Create this exact folder structure!**

---

## STEP 2: Install Python (if not installed)

Check if Python is installed:
```bash
python --version
```

Should show Python 3.8 or higher.

If not installed:
- **Windows**: Download from python.org
- **Mac**: `brew install python3`
- **Linux**: Already installed

---

## STEP 3: Install Required Packages (3 mins)

Open terminal/command prompt in your project folder and run:

```bash
pip install flask flask-sqlalchemy pycryptodome pyotp qrcode pillow --break-system-packages
```

**OR** if you have requirements.txt:
```bash
pip install -r requirements.txt --break-system-packages
```

**Wait for all packages to install!**

---

## STEP 4: Run the Application (1 min)

In the same terminal:
```bash
python app.py
```

You should see:
```
* Running on http://127.0.0.1:5000
```

**Keep this terminal window open!**

---

## STEP 5: Test the Application (4 mins)

### Test 1: Open Browser
Go to: **http://127.0.0.1:5000**

You should see the homepage with security features listed.

### Test 2: Register a User
1. Click "Register"
2. Fill the form:
   - Username: `test1`
   - Email: `test@example.com`
   - Password: `Test123456`
   - Role: Organizer
3. Click "Register & Setup 2FA"

### Test 3: Setup 2FA
1. Download **Google Authenticator** on your phone
   - Android: Play Store
   - iPhone: App Store
2. Scan the QR code shown
3. You'll see a 6-digit code

### Test 4: Login
1. Click "Continue to Login"
2. Enter:
   - Username: `test1`
   - Password: `Test123456`
   - OTP: [6-digit code from phone]
3. You should see the dashboard!

### Test 5: Create Event
1. Click "Create Event"
2. Fill any details
3. Submit
4. Should show success!

**If all 5 tests pass, you're ready! ✅**

---

## 📱 ON EVALUATION DAY - DEMO FLOW

### Before Evaluator Arrives:
1. Start the application: `python app.py`
2. Keep it running
3. Have browser open to http://127.0.0.1:5000
4. Have Google Authenticator app ready
5. Have VIVA_CHEAT_SHEET.md open

### During Evaluation:

**1. Introduction (30 seconds)**
"I've built a Secure Event Pass Generation system that implements all required security components: authentication, authorization, encryption, hashing, digital signatures, and encoding."

**2. Show Homepage (30 seconds)**
Point to security features listed on the page.

**3. Registration Demo (1 minute)**
- Register as organizer
- Show QR code for 2FA
- Scan with phone
- Explain: "Password hashed with PBKDF2-SHA256 and salt, RSA keys generated, OTP secret created"

**4. Login Demo (30 seconds)**
- Enter credentials + OTP from phone
- Explain: "Multi-factor authentication using password and TOTP"

**5. Create Event Demo (1 minute)**
- Create an event
- Explain: "Event details encrypted with AES-256, key encrypted with RSA-2048"
- Show encrypted data vs decrypted view

**6. Generate Pass Demo (1 minute)**
- Register another user as attendee (or open incognito window)
- Generate pass for the event
- Show QR code
- Explain: "QR code encoding, digital signature with SHA256+RSA"

**7. Validate Pass Demo (1 minute)**
- Copy pass code
- Login as organizer
- Validate the pass
- Explain: "Access control check, signature verification, one-time use"

**8. Code Walkthrough (if asked - 2 minutes)**
Open app.py and show:
- Line ~70: `hash_password_with_salt()`
- Line ~85: `encrypt_data_hybrid()`
- Line ~110: `create_digital_signature()`
- Line ~135: `check_permission()`

**Total Time: ~7 minutes**

---

## 🔥 QUICK TROUBLESHOOTING

### Error: "Module not found"
```bash
pip install [module-name] --break-system-packages
```

### Error: "Port 5000 in use"
In app.py, last line, change:
```python
app.run(debug=True, port=5001)
```

### Error: "Can't scan QR code"
Use the manual entry key shown below the QR code.

### Error: "OTP invalid"
Make sure phone time is synced correctly.

---

## 📋 CHECKLIST FOR TOMORROW

Before leaving today:
- [ ] All files downloaded
- [ ] Python installed and working
- [ ] All packages installed successfully
- [ ] Application runs without errors
- [ ] Successfully registered and logged in
- [ ] Phone has Google Authenticator installed
- [ ] Created at least one test event
- [ ] Generated at least one test pass
- [ ] Read VIVA_CHEAT_SHEET.md

On evaluation day:
- [ ] Application running
- [ ] Browser open to homepage
- [ ] Phone with authenticator ready
- [ ] VIVA cheat sheet nearby
- [ ] Confident about all 5 components

---

## 💪 YOU'RE READY!

You have a complete, working system with ALL required components:

✅ Single-Factor Authentication (password)
✅ Multi-Factor Authentication (OTP)
✅ Access Control (ACL + RBAC)
✅ Encryption (AES + RSA hybrid)
✅ Hashing with Salt (PBKDF2-SHA256)
✅ Digital Signatures (SHA256 + RSA)
✅ Encoding (QR Code + Base64)

**All integrated in a real, working web application!**

---

## 🎯 FINAL TIP

When evaluator asks questions, structure your answer:
1. **What**: Brief description
2. **How**: Implementation details
3. **Why**: Security benefit
4. **Where**: Show in code/demo

Example:
Q: "How does your encryption work?"
A: 
- **What**: "I use hybrid encryption"
- **How**: "AES-256 encrypts data, RSA-2048 encrypts the key"
- **Why**: "Combines speed of symmetric with security of asymmetric"
- **Where**: "I can show you in the code - function encrypt_data_hybrid()"

---

**Good luck ra! Dhootha la success pannidu! 🎉**

All the best for tomorrow's evaluation!
