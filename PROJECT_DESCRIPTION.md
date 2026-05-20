# 🔐 Secure Event Pass System - Complete Project Description

## Project Overview

**Secure Event Pass System** is a comprehensive, security-focused web application designed to manage event registration, pass generation, and validation with multiple layers of cryptographic protection. The system demonstrates enterprise-grade security practices by implementing authentication, authorization, encryption, hashing, digital signatures, and secure encoding techniques.

The application enables event organizers to create and manage events while attendees can securely generate and present event passes. All transactions are protected using advanced cryptographic algorithms and security best practices.

---

## 1. Project Purpose & Goals

### Primary Objectives:
- **Secure Event Management**: Provide a platform for organizing events with robust security controls
- **Digital Pass Generation**: Create tamper-proof, digitally signed event passes
- **Multi-Level Access Control**: Implement role-based access with different permissions for admins, organizers, and attendees
- **End-to-End Encryption**: Protect sensitive user data and pass information using hybrid encryption
- **Fraud Prevention**: Prevent pass forgery through digital signatures and QR code validation
- **Authentication Security**: Implement both single-factor and multi-factor authentication mechanisms

### Target Users:
- **Event Organizers**: Create and manage events, validate attendee passes
- **Attendees**: Generate and display event passes securely
- **System Administrators**: Manage users, permissions, and system resources

---

## 2. Technology Stack

### Backend:
- **Framework**: Flask (Python web framework)
- **Database**: SQLite with instance folder for data persistence
- **Cryptography**: 
  - `cryptography` library for RSA and AES encryption
  - `pyotp` for TOTP generation
  - `hashlib` for SHA256 hashing

### Frontend:
- **Templates**: HTML5 with Jinja2 templating
- **Styling**: Custom CSS (pastel theme)
- **QR Code**: Generated dynamically for pass validation

### Security Libraries:
- `Werkzeug` for password hashing
- `PyQRCode` or similar for QR code generation
- `hmac` for cryptographic authentication

---

## 3. Security Features Implementation

### 3.1 Authentication 

#### Single-Factor Authentication
- **Username + Password Login System**
  - Users create accounts with unique usernames
  - Passwords are securely hashed using PBKDF2-SHA256 with salt
  - Login validation against stored hashes
  - Session management for authenticated users
  - Logout functionality to destroy sessions

#### Multi-Factor Authentication (MFA)
- **TOTP-based Two-Factor Authentication**
  - Time-based One-Time Password (TOTP) implementation
  - Compatible with authenticator apps (Google Authenticator, Microsoft Authenticator, Authy)
  - 6-digit codes valid for 30-second time windows
  - Backup codes for account recovery
  - Optional MFA enrollment during user registration or account settings

**Implementation Details:**
- When user enables MFA, system generates unique secret key (base32 encoded)
- Secret shared with authenticator app via QR code
- During login: Username → Password verification → TOTP code verification
- Failed attempts logged for security auditing

**Marks Justification:**
- Single-Factor: Standard authentication mechanism (1.5m)
- Multi-Factor: Added security layer using TOTP (1.5m)

---

### 3.2 Authorization - Access Control

#### Access Control Model (1.5 marks)
- **Three User Roles with Distinct Subjects:**
  1. **Admin**: System administrator with highest privileges
  2. **Organizer**: Event creator and manager
  3. **Attendee**: Event participant and pass holder

- **Multiple Objects Protected:**
  1. **Events**: Creation, modification, deletion, viewing
  2. **Passes**: Generation, validation, revocation
  3. **User Data**: Profile information, sensitive details
  4. **System Settings**: Admin panel, user management

#### Access Control List (ACL) Implementation
```
┌─────────────┬──────────┬────────────┬──────────┐
│  Resource   │  Admin   │ Organizer  │ Attendee │
├─────────────┼──────────┼────────────┼──────────┤
│ Create Event│    ✓     │     ✓      │    ✗     │
│ View Event  │    ✓     │   Own+All  │   Public │
│ Generate Pass│   ✓     │     ✓      │    ✓     │
│ Validate Pass│   ✓     │     ✓      │    ✗     │
│ Manage Users│    ✓     │     ✗      │    ✗     │
│ View Reports│    ✓     │   Own      │    ✗     │
└─────────────┴──────────┴────────────┴──────────┘
```

#### Policy Definition
- **Role-Based Access Control (RBAC)**
  - Admin Policy: Unrestricted access to all resources
  - Organizer Policy: Event management, attendee management, pass validation
  - Attendee Policy: Self-service pass generation, personal profile management

- **Authorization Checks**
  - Decorators on Flask routes enforce role-based access
  - Database queries filtered by user role and ownership
  - API endpoints validate permissions before processing requests


---

### 3.3 Encryption 

#### Key Exchange Mechanism 
- **RSA-2048 Keypair Generation**
  - Each user generates unique 2048-bit RSA keypair upon account creation
  - Public key stored in database for pass validation
  - Private key encrypted and stored securely in user session/database
  - Asymmetric key generation ensures user identity uniqueness

- **Key Management**
  - Secure key storage in encrypted format
  - Keys never transmitted in plaintext
  - Key rotation capability for enhanced security
  - Backup keys for disaster recovery

**Implementation Flow:**
```
User Registration
    ↓
Generate RSA-2048 keypair
    ↓
Store public key in DB
    ↓
Encrypt private key with master key
    ↓
Store encrypted private key
```

#### Encryption & Decryption 
- **Hybrid Encryption Approach**
  - AES-256 (Symmetric): Fast encryption for large data
  - RSA-2048 (Asymmetric): Secure key wrapping

- **Encryption Process**
  1. Generate random 256-bit AES key
  2. Encrypt sensitive data (pass details) with AES-256-CBC
  3. Encrypt AES key with recipient's RSA public key
  4. Transmit encrypted data + encrypted AES key
  5. Include IV (Initialization Vector) for CBC mode

- **Decryption Process**
  1. Receive encrypted data and encrypted AES key
  2. Decrypt AES key using user's RSA private key
  3. Decrypt data using recovered AES key and IV
  4. Validate and process decrypted information

**Security Benefits:**
- Performance: AES-256 provides fast encryption (symmetric)
- Security: RSA-2048 ensures key confidentiality (asymmetric)
- Scalability: Hybrid approach balances speed and security

**Protected Data:**
- Event pass contents
- User personal information
- Transaction records
- Sensitive payment data


---

### 3.4 Hashing & Digital Signature

#### Hashing with Salt 
- **PBKDF2-SHA256 Implementation**
  - Algorithm: PBKDF2 (Password-Based Key Derivation Function 2)
  - Hash Function: SHA256
  - Iterations: 600,000 (exceeds NIST recommendations for 2024)
  - Salt: 32-byte (256-bit) unique salt per user

- **Password Hashing Process**
  1. Generate cryptographically secure random salt
  2. Derive key using PBKDF2-SHA256 with 600,000 iterations
  3. Store salt + hash in database
  4. Never store plaintext passwords

- **Hashing Use Cases**
  - User password protection
  - Pass integrity verification
  - Transaction tamper detection
  - Audit log immutability

**Security Properties:**
- Salted: Prevents rainbow table attacks
- Iterative: Computationally expensive for brute force (600K iterations)
- Modern: SHA256 resistant to collision attacks
- Unique: Each user has different salt

**Example:**
```
User Password: "SecurePass123"
Generated Salt: a3f7b2c9e1d4f6g8h0i2j4k6l8m0n2
Iterations: 600,000
Result Hash: $pbkdf2-sha256$600000$<salt>$<hash>
```

#### Digital Signature 
- **SHA256 + RSA Signature Scheme**
  - Hash Function: SHA256 for message digest
  - Signing Algorithm: RSA-2048 with PKCS#1 v1.5 padding
  - Verification: Public key validation

- **Pass Signature Process**
  1. Collect pass data (event ID, user ID, timestamp, permissions)
  2. Create SHA256 hash of pass data
  3. Encrypt hash with user's RSA private key
  4. Attach signature to pass record
  5. Include timestamp for signature validity

- **Signature Verification Process**
  1. Extract pass data and signature
  2. Decrypt signature using user's RSA public key
  3. Compute SHA256 hash of current pass data
  4. Compare decrypted hash with computed hash
  5. If match: Pass is authentic and unmodified
  6. If mismatch: Pass has been tampered with

- **Fraud Prevention**
  - Organizers can verify pass authenticity
  - Forged passes generate invalid signatures
  - Replay attacks detected via timestamp validation
  - Pass revocation prevents reuse

**Attack Scenarios Prevented:**
| Attack Type | Prevention Method |
|---|---|
| Pass Forgery | RSA signature verification fails |
| Pass Modification | Hash mismatch detected |
| Signature Forgery | Attacker lacks user's private key |
| Replay Attack | Timestamp validation prevents reuse |
| Pass Cloning | Unique signature per pass instance |



---

### 3.5 Encoding Techniques 

#### Encoding Implementation 
- **QR Code Generation**
  - Encodes critical pass information in QR format
  - Data includes: Pass ID, Event ID, User ID, Timestamp, Digital Signature
  - Dynamically generated upon pass creation
  - Scannable with standard QR code readers

- **Base64 Encoding**
  - Encodes binary cryptographic data (RSA signatures, AES keys)
  - Safe for transmission in JSON/HTTP requests
  - Reversible encoding for secure data transport
  - Prevents binary data corruption

**Encoding Process:**
```
Pass Data (JSON)
    ↓
Digitally Sign (RSA)
    ↓
Base64 Encode Signature
    ↓
Generate QR Code
    ↓
Display to User
```

**Pass Information in QR:**
```json
{
  "pass_id": "P12345",
  "event_id": "E001",
  "user_id": "U456",
  "timestamp": "2024-05-20T14:30:00Z",
  "signature": "Base64EncodedSignature...",
  "expires": "2024-06-20T23:59:59Z"
}
```

#### Security Levels & Risks 

**Security Level Analysis:**

| Component | Level | Risk Assessment |
|-----------|-------|-----------------|
| QR Code | Medium | Publicly readable, but content signed |
| Base64 Encoding | Low | Not encryption, only obfuscation |
| Combined with Signature | High | Signature prevents tampering |
| Timestamp Validation | High | Prevents replay attacks |

**Documented Risks:**
- QR codes are scannable by anyone (mitigated by signature)
- Base64 is easily decoded (mitigated by encryption layer)
- Timestamp can be observed (mitigated by short expiration)

#### Possible Attacks & Mitigation 

**Attack 1: Pass Forgery**
- **Attack Method**: Attacker creates fake pass with valid QR code
- **Prevention**: RSA digital signature verification
- **Mitigation**: Organizer validates signature during check-in

**Attack 2: Pass Modification**
- **Attack Method**: Attacker modifies pass data after generation
- **Prevention**: Digital signature becomes invalid
- **Mitigation**: System rejects modified passes

**Attack 3: Replay Attack**
- **Attack Method**: Attacker reuses same pass multiple times
- **Prevention**: Timestamp + expiration validation
- **Mitigation**: Pass marks as "used" after first validation

**Attack 4: QR Code Cloning**
- **Attack Method**: Attacker scans and duplicates QR code
- **Prevention**: Database marks pass as used after validation
- **Mitigation**: Second scan with same pass ID is rejected

**Attack 5: Man-in-the-Middle (MITM)**
- **Attack Method**: Attacker intercepts pass during transmission
- **Prevention**: HTTPS/TLS encryption for transport
- **Mitigation**: SSL certificates for secure connection

**Security Implementation Summary:**
```
Attacker → HTTPS → Server (Encrypted)
           ↓
         TLS Certificate Validation
           ↓
       RSA Signature Verification
           ↓
     Timestamp & Expiration Check
           ↓
      Database "Used" Flag Check
           ↓
      Pass Accepted/Rejected
```



---



The project demonstrates a **fully functional, production-ready** implementation:

**Frontend Features:**
- ✅ User registration with role selection
- ✅ Multi-factor authentication setup interface
- ✅ Event creation and browsing dashboard
- ✅ Pass generation with QR code display
- ✅ Pass validation interface with QR scanner
- ✅ User-friendly error handling and feedback

**Backend Features:**
- ✅ SQLite database with proper schema
- ✅ RESTful endpoints for all operations
- ✅ Session management and authentication
- ✅ Role-based access control enforcement
- ✅ Cryptographic operations (encryption, signing)
- ✅ Error handling and logging

**Database Schema:**
```
Users Table: user_id, username, password_hash, salt, role, rsa_public_key, totp_secret
Events Table: event_id, organizer_id, event_name, description, date, capacity
Passes Table: pass_id, user_id, event_id, digital_signature, status, created_at, validated_at
AccessLogs Table: log_id, user_id, action, resource, timestamp, status
```


**Attack Surface Protection:**
```
┌─────────────────────────────────────────────────────┐
│           External Threat (Attacker)                │
├─────────────────────────────────────────────────────┤
│  HTTPS/TLS Layer (Transport Security)               │
├─────────────────────────────────────────────────────┤
│  Authentication Layer (MFA Protection)              │
├─────────────────────────────────────────────────────┤
│  Authorization Layer (ACL Enforcement)              │
├─────────────────────────────────────────────────────┤
│  Encryption Layer (AES-256 + RSA-2048)              │
├─────────────────────────────────────────────────────┤
│  Integrity Layer (Signatures + Hashing)             │
├─────────────────────────────────────────────────────┤
│  Database (Protected with Credentials)              │
└─────────────────────────────────────────────────────┘
```




---

## 4. User Workflows

### Workflow 1: Event Attendee Registration & Pass Generation

```
┌─────────────────────────────────────────────────────────┐
│  1. User Registration (Attendee)                        │
│     - Create account with username + password           │
│     - Password hashed with PBKDF2-SHA256 (600K iter)    │
│     - RSA-2048 keypair generated                        │
│     - Role assigned: ATTENDEE                           │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  2. Multi-Factor Authentication Setup (Optional)        │
│     - Enable TOTP on account settings                   │
│     - Receive secret key (base32)                       │
│     - Scan QR code with authenticator app               │
│     - Verify with 6-digit code                          │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  3. Browse Events                                       │
│     - View available events                             │
│     - Filter by date, category, capacity                │
│     - Read event details                                │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  4. Generate Event Pass                                 │
│     - Select event to attend                            │
│     - System creates pass record                        │
│     - Calculate SHA256 hash of pass data                │
│     - Sign hash with user's RSA private key             │
│     - Encode signature in Base64                        │
│     - Generate QR code with pass info                   │
│     - Return encoded pass to user                       │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  5. Present Pass at Event                               │
│     - Show QR code on mobile device                     │
│     - Organizer scans QR code                           │
│     - System verifies digital signature                 │
│     - Timestamp validation (not expired)                │
│     - Check if pass already used                        │
│     - Mark pass as validated                            │
│     - Grant entry to attendee                           │
└─────────────────────────────────────────────────────────┘
```

### Workflow 2: Event Organizer Management

```
┌─────────────────────────────────────────────────────────┐
│  1. Organizer Registration                              │
│     - Create account with username + password           │
│     - Select role: ORGANIZER                            │
│     - Receive permission set for event creation         │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  2. Create Event                                        │
│     - Fill event details (name, date, capacity)         │
│     - Set ticket price/free                             │
│     - Configure entry rules                             │
│     - Encrypt event data with AES-256                   │
│     - Store in database with organizer ID               │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  3. Validate Attendee Passes                            │
│     - Receive QR code from attendee                     │
│     - Decode QR and extract pass data                   │
│     - Retrieve pass from database                       │
│     - Verify RSA digital signature                      │
│     - Check timestamp validity                          │
│     - Query "used" status                               │
│     - Approve/Reject entry                              │
│     - Log validation event                              │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  4. View Event Analytics                                │
│     - Total registrations                               │
│     - Validated passes                                  │
│     - Attendance rate                                   │
│     - Flagged fraudulent attempts                       │
└─────────────────────────────────────────────────────────┘
```

### Workflow 3: Admin System Management

```
┌─────────────────────────────────────────────────────────┐
│  1. Admin Registration                                  │
│     - System-created admin account                      │
│     - Full system permissions                           │
│     - Access to all resources                           │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  2. User Management                                     │
│     - View all registered users                         │
│     - Modify user roles and permissions                 │
│     - Reset user passwords (with MFA backup codes)      │
│     - Revoke suspicious accounts                        │
│     - View user activity logs                           │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  3. System Monitoring                                   │
│     - Security event logs                               │
│     - Failed authentication attempts                    │
│     - Unauthorized access attempts                      │
│     - Cryptographic operation logs                      │
│     - Database audit trail                              │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  4. Security Configuration                              │
│     - Update encryption keys                            │
│     - Configure MFA policies                            │
│     - Set password requirements                         │
│     - Manage SSL certificates                           │
│     - Configure backup systems                          │
└─────────────────────────────────────────────────────────┘
```

---

## 5. Security Architecture

### 5.1 Authentication Architecture

```
Login Request
    ↓
┌─────────────────────────────────────────┐
│ Step 1: Username Validation              │
│ - Query database for user               │
│ - Check if account exists               │
│ - Verify account not locked             │
└─────────────────────────────────────────┘
    ↓ Success
┌─────────────────────────────────────────┐
│ Step 2: Password Verification            │
│ - Hash provided password with stored salt│
│ - Use PBKDF2-SHA256 (600K iterations)   │
│ - Compare with stored hash              │
│ - Constant-time comparison (prevent timing attacks) │
└─────────────────────────────────────────┘
    ↓ Success (if MFA enabled)
┌─────────────────────────────────────────┐
│ Step 3: TOTP Code Verification          │
│ - Request 6-digit code from user        │
│ - Validate against user's TOTP secret   │
│ - Check within 30-second window         │
│ - Prevent code reuse (grace period)     │
└─────────────────────────────────────────┘
    ↓ Success
┌─────────────────────────────────────────┐
│ Step 4: Session Creation                 │
│ - Generate secure session token         │
│ - Store session with user ID            │
│ - Set cookie with HttpOnly, Secure flags│
│ - Log successful login                  │
└─────────────────────────────────────────┘
    ↓
✓ User Authenticated
```

### 5.2 Authorization Architecture

```
HTTP Request with Session
    ↓
┌─────────────────────────────────────────┐
│ Route Handler Called                     │
│ @authorize_role('admin', 'organizer')   │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ Authorization Check                      │
│ - Extract user from session              │
│ - Query user role from database          │
│ - Check role against allowed list        │
│ - Check object-level permissions         │
└─────────────────────────────────────────┘
    ↓ Authorized
┌─────────────────────────────────────────┐
│ Resource Access                          │
│ - Query filtered by user ownership       │
│ - Apply role-based data masking          │
│ - Log access for audit trail             │
│ - Execute business logic                 │
└─────────────────────────────────────────┘
    ↓
✓ Resource Returned
```

### 5.3 Encryption Architecture

```
Sensitive Data → AES-256 Encryption
┌─────────────────────────────────────────┐
│ AES-256-CBC Encryption                   │
│ - Generate 256-bit random key            │
│ - Generate 128-bit random IV             │
│ - Encrypt data using AES-256-CBC         │
│ - Encrypt AES key with RSA public key    │
│ - Return ciphertext + encrypted key      │
└─────────────────────────────────────────┘
    ↓ Transmission (over HTTPS)
    ↓
┌─────────────────────────────────────────┐
│ RSA Decryption                            │
│ - Decrypt AES key with RSA private key   │
│ - Verify key integrity                   │
│ - Use key to decrypt data                │
│ - Validate padding and format            │
└─────────────────────────────────────────┘
    ↓
✓ Original Data Recovered
```

---

## 6. Security Best Practices Implemented

### 6.1 Password Security
- ✅ PBKDF2-SHA256 with 600,000 iterations
- ✅ Unique salt per user (256-bit random)
- ✅ Never store plaintext passwords
- ✅ Constant-time comparison to prevent timing attacks
- ✅ Enforce password complexity requirements

### 6.2 Session Management
- ✅ Secure session tokens (cryptographically random)
- ✅ HttpOnly cookies (prevent JavaScript access)
- ✅ Secure flag (HTTPS only transmission)
- ✅ SameSite attribute (prevent CSRF)
- ✅ Session timeout after inactivity
- ✅ Logout clears session completely

### 6.3 Cryptographic Operations
- ✅ Using established libraries (cryptography, pyotp)
- ✅ Proper key management and storage
- ✅ Secure random number generation
- ✅ No hardcoded secrets in code
- ✅ Key rotation capabilities

### 6.4 Transport Security
- ✅ HTTPS/TLS for all communications
- ✅ SSL certificate validation
- ✅ Protection against MITM attacks
- ✅ Secure headers (HSTS, X-Frame-Options, etc.)

### 6.5 Input Validation
- ✅ Whitelist validation for user roles
- ✅ SQL injection prevention (parameterized queries)
- ✅ XSS protection (HTML escaping)
- ✅ CSRF token validation on state-changing requests

### 6.6 Data Protection
- ✅ Encryption at rest (AES-256)
- ✅ Encryption in transit (HTTPS/TLS)
- ✅ Secure deletion of sensitive data
- ✅ Database access controls

---

## 7. Testing & Validation

### Security Test Cases
- ✅ Authentication bypass attempts
- ✅ Authorization escalation attempts
- ✅ Encryption key leakage
- ✅ Signature forgery attempts
- ✅ Pass duplication attacks
- ✅ TOTP code reuse prevention
- ✅ SQL injection prevention
- ✅ XSS vulnerability scanning

### Performance Testing
- ✅ PBKDF2 iteration time acceptable
- ✅ RSA key generation time acceptable
- ✅ AES encryption/decryption speed
- ✅ Database query optimization
- ✅ Concurrent user handling

---

## 8. Deployment & Maintenance

### Production Considerations
- Set `FLASK_ENV=production`
- Use strong database encryption
- Regular security audits
- Dependency vulnerability scanning
- Backup and disaster recovery
- Monitoring and alerting
- Incident response procedures

### Security Maintenance
- Regular dependency updates
- Cryptographic algorithm review (2+ years)
- Penetration testing (annual)
- User data privacy audit (annual)
- Incident response drills

---

## 9. Conclusion

The **Secure Event Pass System** demonstrates a comprehensive implementation of modern security practices across all layers:

✅ **Authentication**: Single-factor + Multi-factor (TOTP)
✅ **Authorization**: Role-based ACL with multiple subjects/objects
✅ **Encryption**: Hybrid encryption (AES-256 + RSA-2048)
✅ **Hashing**: PBKDF2-SHA256 with unique salts (600K iterations)
✅ **Signatures**: RSA-2048 digital signatures with SHA256
✅ **Encoding**: QR codes + Base64 with documented risks

The system is **production-ready** and provides a **secure, scalable platform** for event management with strong fraud prevention and user data protection.

---


