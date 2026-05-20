# 🎯 VIVA CHEAT SHEET - Quick Reference

## Component 1: AUTHENTICATION (3m)

### Single-Factor (1.5m)
**What**: Username + Password login
**How**: 
- Password hashed with PBKDF2-SHA256
- 600,000 iterations
- Unique salt per user (64 chars)
**Code**: `hash_password_with_salt()` function
**Demo**: Show registration, explain password never stored in plain text

### Multi-Factor (1.5m)
**What**: Password + OTP (TOTP)
**How**: 
- Factor 1: Password (something you know)
- Factor 2: TOTP from Google Authenticator (something you have)
- Uses pyotp library
- Time-based, changes every 30 seconds
**Code**: `verify_otp()` function
**Demo**: Show QR code setup, then login with OTP

---

## Component 2: AUTHORIZATION - ACCESS CONTROL (3m)

### Access Control Model (1.5m)
**What**: Access Control List (ACL)
**Subjects**: 3 types of users
1. Admin - full access
2. Organizer - manage events
3. Attendee - view and generate passes

**Objects**: 3 types
1. Events
2. Event Passes
3. User data

**Implementation**: AccessControl table with (subject_id, object_type, object_id, permission)
**Code**: `check_permission()` function

### Policy & Enforcement (1.5m)
**Permissions**: read, write, delete, validate

**Rules**:
- Organizer can validate passes for THEIR events only
- Admin can do everything
- Attendee can only generate passes and view own data
- Enforced programmatically before every operation

**Code**: `grant_permission()`, `@role_required` decorator
**Demo**: Try accessing event as different roles

---

## Component 3: ENCRYPTION (3m)

### Key Exchange (1.5m)
**What**: RSA-2048 keypair generation
**How**: 
- Generated during registration
- Public key stored in database
- Private key stored in database (in real system, would be encrypted)
**Code**: `generate_rsa_keypair()` function
**Demo**: Show keys in database or during registration

### Encryption/Decryption (1.5m)
**What**: Hybrid Encryption
**How**: 
1. Generate random AES-256 key
2. Encrypt data with AES (fast, symmetric)
3. Encrypt AES key with RSA public key (secure, asymmetric)
4. Store both encrypted data and encrypted key

**Decryption**:
1. Decrypt AES key with RSA private key
2. Decrypt data with AES key

**Why Hybrid**: Combines speed of AES with security of RSA
**Code**: `encrypt_data_hybrid()`, `decrypt_data_hybrid()`
**Demo**: Create event, show encrypted details, show decryption for organizer

---

## Component 4: HASHING & DIGITAL SIGNATURE (3m)

### Hashing with Salt (1.5m)
**What**: Secure password storage
**Algorithm**: PBKDF2-SHA256
**Iterations**: 600,000 (OWASP recommendation)
**Salt**: 64 character random hex string, unique per user

**Why Salt**: 
- Prevents rainbow table attacks
- Same password = different hashes for different users
- Even if DB leaked, passwords safe

**Code**: `generate_salt()`, `hash_password_with_salt()`
**Demo**: Show different hashes for same password with different salts

### Digital Signature (1.5m)
**What**: Ensures pass authenticity and integrity
**How**: 
1. Hash the pass code with SHA256
2. Sign the hash with user's RSA private key
3. Store signature with pass

**Verification**:
1. Hash the pass code
2. Verify signature with user's RSA public key
3. If match = authentic, not tampered

**Prevents**: Forgery, tampering
**Code**: `create_digital_signature()`, `verify_digital_signature()`
**Demo**: Show signature on pass, show verification success/failure

---

## Component 5: ENCODING (3m)

### Encoding Implementation (1m)
**Technique Used**: QR Code + Base64
**How**: 
1. Create pass data as JSON
2. Generate QR code image
3. Encode image as Base64 string
4. Store in database

**Why QR Code**: Easy scanning at event venue
**Why Base64**: Store binary image in text database
**Code**: `generate_qr_code()` function
**Demo**: Show QR code on pass, explain it contains pass data

### Security Levels (1m)
**Low Security**: Base64 (encoding, not encryption)
- Can be decoded easily
- Used for data format, not secrecy

**Medium Security**: QR Code
- Visible but needs scanner
- Contains pass code

**High Security**: Digital signature
- Ensures authenticity
- Cannot be forged

### Possible Attacks (1m)
**Attack 1**: Pass Code Guessing
- **Prevention**: Random generation with secrets.token_hex()

**Attack 2**: Pass Forgery
- **Prevention**: Digital signature verification

**Attack 3**: Pass Reuse
- **Prevention**: One-time use flag (is_used)

**Attack 4**: QR Code Duplication
- **Prevention**: Each validation checks signature + usage status

---

## 🔥 COMMON VIVA QUESTIONS & ANSWERS

### Q: Why not just use password without OTP?
**A**: Single factor can be stolen/guessed. OTP adds physical device requirement, making it much harder to breach.

### Q: Why hybrid encryption instead of just RSA?
**A**: RSA is slow for large data. AES is fast. We use AES for data (speed) and RSA to protect the AES key (security).

### Q: How does salt prevent rainbow tables?
**A**: Rainbow tables pre-compute hashes. With unique salts, attacker needs to compute hash for each user separately, making it impractical.

### Q: Can someone copy the QR code and use it?
**A**: They can copy QR, but pass can only be used once (is_used flag). Also, digital signature ensures it's not forged.

### Q: What if someone gets the database?
**A**: 
- Passwords: Protected by salt + 600k iterations of PBKDF2
- Event data: Encrypted with RSA, needs private key
- Passes: Have digital signatures, can't be forged

### Q: Difference between encoding and encryption?
**A**: 
- **Encoding** (Base64, QR): Format conversion, anyone can decode
- **Encryption** (AES, RSA): Security transformation, needs key to decrypt

### Q: How do you implement NIST SP 800-63-2?
**A**: 
- Credential Service Provider: Our registration system
- Verifier: Our authentication system
- Relying Party: Our application
- Multi-factor authentication implemented
- Secure session management

### Q: What's the access control matrix?
**A**: 
```
           Events  Passes  Users
Admin      RWD     RWD     RWD
Organizer  RW*     RV*     R
Attendee   R*      RW**    R*

* = only for their own objects
** = only create, view own
V = validate
```

---

## 📊 SECURITY FLOW DIAGRAM

### Registration:
User Input → Generate Salt → Hash Password (PBKDF2) → Generate RSA Keys → Generate OTP Secret → Store in DB → Show QR Code

### Login:
Enter Credentials → Verify Password (hash check) → Verify OTP (TOTP) → Create Session → Redirect to Dashboard

### Create Event:
Event Details → Generate AES Key → Encrypt Data (AES) → Encrypt AES Key (RSA) → Store Both → Grant ACL Permissions

### Generate Pass:
Generate Pass Code → Create JSON Data → Generate QR (encode) → Sign with RSA → Store Pass → Grant Read Permission

### Validate Pass:
Enter Pass Code → Check ACL Permission → Verify Digital Signature → Check Usage Status → Mark as Used

---

## 🎬 DEMO SEQUENCE FOR EVAL

1. **Start**: Open browser to http://127.0.0.1:5000
2. **Register**: Show password hashing, salt generation, RSA keys, OTP setup
3. **2FA Setup**: Scan QR code with phone
4. **Login**: Demonstrate multi-factor (password + OTP)
5. **Create Event**: Show encryption of event details
6. **Generate Pass**: Show QR code generation, digital signature
7. **View Pass**: Point out all security features
8. **Validate**: Show access control, signature verification
9. **Explain**: Point to code and explain each function

---

## 💡 KEY POINTS TO EMPHASIZE

✅ All 5 main components implemented
✅ Real-world application (not toy example)
✅ Production-grade security practices
✅ Following NIST standards
✅ Cohesive integration (not separate demos)
✅ Access control enforced programmatically
✅ Multiple layers of security

---

## 🔧 IF EVALUATOR ASKS TO SHOW CODE

**Most Important Functions to Know**:

1. `hash_password_with_salt()` - Line ~70
2. `verify_otp()` - Line ~115
3. `encrypt_data_hybrid()` - Line ~85
4. `create_digital_signature()` - Line ~110
5. `check_permission()` - Line ~135

**Show in app.py and explain each one clearly**

---

Good luck da! You got this! 🎉
