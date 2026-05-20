# 🎫 Secure Event Pass Generation & Access Validation System


---

## 🔐 Security Features Implemented

Note: This project was developed as part of a cyber security evaluation.

Overview
--------
Secure Event Pass System is a web application that demonstrates secure event management, pass generation, and validation using modern cryptographic techniques and best practices. The system is designed for demonstration and evaluation of concepts including authentication, authorization, encryption, hashing, digital signatures, and secure encoding.

Security features 
-------------------------
- Authentication: Username/password with optional TOTP-based MFA for stronger account protection.
- Authorization: Role-based access control (Admin, Organizer, Attendee) enforced at route and object level.
- Encryption: Hybrid encryption using AES-256 for data and RSA-2048 for key protection.
- Hashing & Signatures: PBKDF2-SHA256 for password hashing; SHA256 + RSA signatures for pass authenticity.
- Encoding: QR codes for pass presentation and Base64 for safe transmission of binary data.

## 🚀 Installation & Setup 

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
License
-------
This project is made  for educational purposes as part of a cyber security evaluation. Check repository settings for license details.




