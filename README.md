# 🎫 Secure Event Pass Generation & Access Validation System

## Lab Evaluation 1 - 23CSE313 Foundations of Cyber Security

A comprehensive web-based application implementing all required security concepts: Authentication, Authorization, Encryption, Hashing, Digital Signatures, and Encoding.

---

## 🔐 Security Features Implemented

### ✅ All 20 Marks Components Covered

#### 1. **Authentication (3 marks)**
- ✅ **Single-Factor Authentication (1.5m)**: Username + Password login
- ✅ **Multi-Factor Authentication (1.5m)**: Password + TOTP (Time-based OTP from authenticator app)
- 📱 **Implementation**: Google Authenticator / Authy compatible

#### 2. **Authorization - Access Control (3 marks)**
- ✅ **Access Control Model (1.5m)**: Access Control List (ACL) with 3+ subjects and objects
  - Subjects: Admin, Organizer, Attendee users
  - Objects: Events, Passes, User data
- ✅ **Policy Definition (1.5m)**: Role-based permissions + ACL implementation
  - Admin: Full access to all resources
  - Organizer: Create/manage events, validate passes
  - Attendee: Generate passes, view own data

#### 3. **Encryption (3 marks)**
- ✅ **Key Exchange Mechanism (1.5m)**: RSA-2048 keypair generation per user
- ✅ **Encryption & Decryption (1.5m)**: Hybrid encryption
  - AES-256 for data encryption (fast, symmetric)
  - RSA-2048 for key encryption (secure, asymmetric)

#### 4. **Hashing & Digital Signature (3 marks)**
- ✅ **Hashing with Salt (1.5m)**: PBKDF2-SHA256 (600,000 iterations) + unique salt per user
- ✅ **Digital Signature (1.5m)**: SHA256 hash + RSA signing for pass authenticity

#### 5. **Encoding Techniques (3 marks)**
- ✅ **Encoding Implementation (1m)**: QR Code + Base64 encoding for event passes
- ✅ **Security Levels & Risks (1m)**: Documented in code and interface
- ✅ **Possible Attacks (1m)**: Pass forgery prevention, replay attack mitigation

#### 6. **Viva (2m + 3m = 5 marks)**
- Complete implementation ready for demonstration
- All security concepts integrated cohesively
- Clear documentation for explaining design choices

---

## 🚀 Installation & Setup (STEP-BY-STEP)

### Step 1: Prerequisites
Make sure you have Python 3.8+ installed:
```bash
python --version
```

### Step 2: Install Required Packages
```bash
pip install flask flask-sqlalchemy pycryptodome pyotp qrcode pillow --break-system-packages
```

Or use requirements.txt:
```bash
pip install -r requirements.txt --break-system-packages
```

### Step 3: Run the Application
```bash
python app.py
```

The application will start at: **http://127.0.0.1:5000**

---

## 📱 User Guide for Evaluation Demo

### Demo Flow (Follow this sequence):

#### 1️⃣ **Register as Organizer**
1. Go to http://127.0.0.1:5000
2. Click "Register"
3. Fill details:
   - Username: `organizer1`
   - Email: `org@example.com`
   - Password: `SecurePass123`
   - Role: **Organizer**
4. Click "Register & Setup 2FA"
5. **IMPORTANT**: Scan QR code with Google Authenticator app
   - Download: Google Authenticator (Android/iOS)
   - Or use the manual entry key shown

#### 2️⃣ **Login with 2FA**
1. Enter username and password
2. Open Google Authenticator app
3. Enter the 6-digit code
4. Click "Login Securely"

#### 3️⃣ **Create Event (Demonstrates Encryption)**
1. Click "Create Event"
2. Fill event details:
   - Name: `Tech Conference 2026`
   - Date: Select future date
   - Venue: `Main Hall`
   - Details: `This is encrypted data with AES-256`
3. Click "Create Event"
4. **Security Applied**:
   - Event details encrypted with AES-256
   - AES key encrypted with RSA-2048
   - Only organizer can decrypt

#### 4️⃣ **Register as Attendee (New User)**
1. Logout (top right)
2. Register again:
   - Username: `attendee1`
   - Email: `att@example.com`
   - Password: `SecurePass456`
   - Role: **Attendee**
3. Setup 2FA and login

#### 5️⃣ **Generate Event Pass (Demonstrates Digital Signature & QR Code)**
1. View the event
2. Click "Generate Pass Now"
3. **Security Applied**:
   - Unique pass code generated
   - QR code created (encoding)
   - Digital signature using SHA256+RSA
   - Pass data encoded in Base64

#### 6️⃣ **View Pass (Shows All Security Features)**
1. Click "View Pass"
2. **Observe**:
   - QR code (encoding technique)
   - Digital signature verification
   - Pass code with encryption

#### 7️⃣ **Validate Pass (Demonstrates Authorization)**
1. Logout and login as **organizer1**
2. Click "Validate Pass"
3. Copy the pass code from attendee's pass
4. Paste and validate
5. **Security Applied**:
   - Authorization check (ACL)
   - Digital signature verification
   - One-time use enforcement

---

## 📊 Security Components Mapping

| Component | Implementation | Code Location | Demo Step |
|-----------|---------------|---------------|-----------|
| **Password Hashing** | PBKDF2-SHA256 + Salt | `hash_password_with_salt()` | Registration |
| **Multi-Factor Auth** | TOTP (OTP) | `verify_otp()` | Login |
| **RSA Encryption** | 2048-bit keypair | `generate_rsa_keypair()` | Registration |
| **AES Encryption** | 256-bit symmetric | `encrypt_data_hybrid()` | Create Event |
| **Digital Signature** | SHA256 + RSA | `create_digital_signature()` | Generate Pass |
| **QR Code** | Base64 encoding | `generate_qr_code()` | View Pass |
| **Access Control** | ACL + RBAC | `check_permission()` | All operations |

---

## 🎯 For VIVA Questions - Quick Answers

### Q: How does Multi-Factor Authentication work?
**A**: We use two factors:
1. **Password** (something you know) - hashed with PBKDF2-SHA256
2. **OTP** (something you have) - TOTP from authenticator app
Both must be correct to login.

### Q: Explain your encryption approach?
**A**: Hybrid encryption:
- **AES-256** encrypts event data (fast, symmetric)
- **RSA-2048** encrypts the AES key (secure, asymmetric)
- Only the organizer with the private key can decrypt

### Q: How do you prevent pass forgery?
**A**: 
1. Digital signature using SHA256 hash + RSA signing
2. Each pass signed with user's private key
3. Verification using public key during validation
4. Any tampering invalidates the signature

### Q: Explain Access Control implementation?
**A**: 
- **Role-Based**: Admin, Organizer, Attendee roles
- **ACL**: Permissions stored in AccessControl table
- Example: Only organizers can validate passes for their events
- Checked before every operation

### Q: What encoding techniques are used?
**A**: 
1. **Base64**: For storing binary data (QR images, signatures)
2. **QR Code**: Encoding pass data for scanning
3. **JSON**: Encoding pass information

### Q: How is password security ensured?
**A**: 
- Unique random salt per user (64 characters)
- PBKDF2-SHA256 algorithm
- 600,000 iterations (OWASP recommendation)
- Salt stored separately, prevents rainbow table attacks

---

## 📁 Project Structure

```
event_pass_system/
├── app.py                 # Main application (all security logic)
├── requirements.txt       # Dependencies
├── templates/             # HTML templates
│   ├── base.html         # Base template with styling
│   ├── index.html        # Homepage
│   ├── register.html     # User registration
│   ├── show_qr.html      # 2FA QR code display
│   ├── login.html        # Login page
│   ├── dashboard.html    # User dashboard
│   ├── create_event.html # Event creation
│   ├── view_event.html   # Event details
│   ├── view_pass.html    # Pass display
│   ├── validate_pass.html # Pass validation
│   └── validation_result.html # Validation result
└── event_pass_system.db  # SQLite database (auto-created)
```

---

## 🔍 Database Schema

### Users Table
- `id`, `username`, `email`, `password_hash`, `salt`, `role`
- `otp_secret`, `public_key`, `private_key`

### Events Table
- `id`, `name`, `date`, `venue`, `organizer_id`
- `encrypted_details`, `encryption_key`

### EventPass Table
- `id`, `pass_code`, `event_id`, `attendee_id`
- `qr_code`, `digital_signature`, `is_used`, `validated_at`

### AccessControl Table
- `id`, `subject_id`, `object_type`, `object_id`, `permission`

---

## 🎬 Quick Demo Script (5 minutes)

1. **"I'll demonstrate authentication"** → Register + show 2FA QR
2. **"Login with multi-factor"** → Enter password + OTP
3. **"Create encrypted event"** → Show encryption notification
4. **"Generate pass with signature"** → Show QR + digital signature
5. **"Validate with access control"** → Show authorization check
6. **"All security components integrated"** → Point to security badges

---

## 🛠️ Troubleshooting

### Issue: Module not found
```bash
pip install flask flask-sqlalchemy pycryptodome pyotp qrcode pillow --break-system-packages
```

### Issue: Port already in use
Change port in app.py last line:
```python
app.run(debug=True, port=5001)  # Changed from 5000
```

### Issue: Can't scan QR code
Use manual entry key shown below the QR code in your authenticator app.

---

## 📞 Support

For evaluation questions, ensure you can explain:
1. How each security component works
2. Where it's implemented in code
3. Why you chose this approach
4. What attacks it prevents

**Good luck with your evaluation! 🎉**
