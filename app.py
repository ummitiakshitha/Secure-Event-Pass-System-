"""
Secure Event Pass Generation & Access Validation System
Implements: Authentication, Authorization, Encryption, Hashing, Encoding
Following NIST SP 800-63-2 E-Authentication Architecture
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import pyotp
import qrcode
import io
import base64
import secrets
import json
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///event_pass_system.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ============= DATABASE MODELS =============

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    salt = db.Column(db.String(64), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin, organizer, attendee
    otp_secret = db.Column(db.String(32))
    public_key = db.Column(db.Text)
    private_key = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    venue = db.Column(db.String(200))
    organizer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    encrypted_details = db.Column(db.Text)  # Encrypted event details
    encryption_key = db.Column(db.Text)  # RSA encrypted AES key
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    organizer = db.relationship('User', backref=db.backref('events', lazy=True))

class EventPass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pass_code = db.Column(db.String(100), unique=True, nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    attendee_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    qr_code = db.Column(db.Text)  # Base64 encoded QR code
    digital_signature = db.Column(db.Text)  # Hash-based signature
    is_used = db.Column(db.Boolean, default=False)
    validated_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    event = db.relationship('Event', backref=db.backref('passes', lazy=True))
    attendee = db.relationship('User', foreign_keys=[attendee_id], backref=db.backref('passes', lazy=True))

class AccessControl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # User
    object_type = db.Column(db.String(50))  # event, pass, user
    object_id = db.Column(db.Integer)
    permission = db.Column(db.String(20))  # read, write, delete, validate

# ============= SECURITY FUNCTIONS =============

def generate_salt():
    """Generate random salt for password hashing"""
    return secrets.token_hex(32)

def hash_password_with_salt(password, salt):
    """Hash password with salt using PBKDF2-SHA256"""
    return generate_password_hash(password + salt, method='pbkdf2:sha256:600000')

def generate_rsa_keypair():
    """Generate RSA key pair for encryption"""
    key = RSA.generate(2048)
    private_key = key.export_key().decode('utf-8')
    public_key = key.publickey().export_key().decode('utf-8')
    return private_key, public_key

def encrypt_data_hybrid(data, public_key_pem):
    """Hybrid encryption: AES for data, RSA for key"""
    # Generate AES key
    aes_key = get_random_bytes(32)
    
    # Encrypt data with AES
    cipher_aes = AES.new(aes_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(data.encode('utf-8'))
    
    # Encrypt AES key with RSA
    public_key = RSA.import_key(public_key_pem)
    cipher_rsa = PKCS1_OAEP.new(public_key)
    encrypted_aes_key = cipher_rsa.encrypt(aes_key)
    
    # Combine nonce, tag, ciphertext
    encrypted_data = base64.b64encode(cipher_aes.nonce + tag + ciphertext).decode('utf-8')
    encrypted_key = base64.b64encode(encrypted_aes_key).decode('utf-8')
    
    return encrypted_data, encrypted_key

def decrypt_data_hybrid(encrypted_data, encrypted_key, private_key_pem):
    """Hybrid decryption"""
    # Decrypt AES key with RSA
    private_key = RSA.import_key(private_key_pem)
    cipher_rsa = PKCS1_OAEP.new(private_key)
    aes_key = cipher_rsa.decrypt(base64.b64decode(encrypted_key))
    
    # Decrypt data with AES
    encrypted_bytes = base64.b64decode(encrypted_data)
    nonce = encrypted_bytes[:16]
    tag = encrypted_bytes[16:32]
    ciphertext = encrypted_bytes[32:]
    
    cipher_aes = AES.new(aes_key, AES.MODE_EAX, nonce=nonce)
    data = cipher_aes.decrypt_and_verify(ciphertext, tag)
    
    return data.decode('utf-8')

def create_digital_signature(data, private_key_pem):
    """Create digital signature using SHA256 hash"""
    # Hash the data
    hash_obj = SHA256.new(data.encode('utf-8'))
    
    # Sign with private key
    private_key = RSA.import_key(private_key_pem)
    signature = pkcs1_15.new(private_key).sign(hash_obj)
    
    return base64.b64encode(signature).decode('utf-8')

def verify_digital_signature(data, signature, public_key_pem):
    """Verify digital signature"""
    try:
        hash_obj = SHA256.new(data.encode('utf-8'))
        public_key = RSA.import_key(public_key_pem)
        pkcs1_15.new(public_key).verify(hash_obj, base64.b64decode(signature))
        return True
    except:
        return False

def generate_qr_code(data):
    """Generate QR code (encoding technique)"""
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
    
    return img_base64

def generate_otp_secret():
    """Generate OTP secret for 2FA"""
    return pyotp.random_base32()

def verify_otp(secret, otp):
    """Verify OTP for multi-factor authentication"""
    totp = pyotp.TOTP(secret)
    return totp.verify(otp, valid_window=1)

# ============= ACCESS CONTROL =============

def check_permission(user_id, object_type, object_id, permission):
    """Check if user has permission (Access Control List implementation)"""
    acl = AccessControl.query.filter_by(
        subject_id=user_id,
        object_type=object_type,
        object_id=object_id,
        permission=permission
    ).first()
    
    return acl is not None

def grant_permission(user_id, object_type, object_id, permission):
    """Grant permission to user"""
    acl = AccessControl(
        subject_id=user_id,
        object_type=object_type,
        object_id=object_id,
        permission=permission
    )
    db.session.add(acl)
    db.session.commit()

def login_required(f):
    """Decorator for routes requiring authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(role):
    """Decorator for role-based access control"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please login first', 'error')
                return redirect(url_for('login'))
            
            user = User.query.get(session['user_id'])
            if user.role != role and user.role != 'admin':
                flash('Access denied', 'error')
                return redirect(url_for('dashboard'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# ============= ROUTES =============

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role', 'attendee')
        
        # Check if user exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('register'))
        
        # Generate salt and hash password
        salt = generate_salt()
        password_hash = hash_password_with_salt(password, salt)
        
        # Generate RSA keypair
        private_key, public_key = generate_rsa_keypair()
        
        # Generate OTP secret for 2FA
        otp_secret = generate_otp_secret()
        
        # Create user
        user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            salt=salt,
            role=role,
            otp_secret=otp_secret,
            public_key=public_key,
            private_key=private_key
        )
        
        db.session.add(user)
        db.session.commit()
        
        # Store OTP secret for showing QR code
        session['temp_otp_secret'] = otp_secret
        session['temp_username'] = username
        
        flash('Registration successful! Please scan the QR code for 2FA setup', 'success')
        return redirect(url_for('show_qr'))
    
    return render_template('register.html')

@app.route('/show-qr')
def show_qr():
    """Show QR code for 2FA setup"""
    if 'temp_otp_secret' not in session:
        return redirect(url_for('login'))
    
    otp_secret = session.get('temp_otp_secret')
    username = session.get('temp_username')
    
    # Generate OTP URI
    totp = pyotp.TOTP(otp_secret)
    otp_uri = totp.provisioning_uri(username, issuer_name="Event Pass System")
    
    # Generate QR code
    qr_code = generate_qr_code(otp_uri)
    
    return render_template('show_qr.html', qr_code=qr_code, secret=otp_secret)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        otp = request.form.get('otp')
        
        user = User.query.filter_by(username=username).first()
        
        if not user:
            flash('Invalid credentials', 'error')
            return redirect(url_for('login'))
        
        # Verify password (Factor 1)
        if not check_password_hash(user.password_hash, password + user.salt):
            flash('Invalid credentials', 'error')
            return redirect(url_for('login'))
        
        # Verify OTP (Factor 2 - Multi-Factor Authentication)
        if not verify_otp(user.otp_secret, otp):
            flash('Invalid OTP', 'error')
            return redirect(url_for('login'))
        
        # Login successful
        session['user_id'] = user.id
        session['username'] = user.username
        session['role'] = user.role
        
        flash('Login successful!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    user = User.query.get(session['user_id'])
    
    # Get user's events based on role
    if user.role == 'admin':
        events = Event.query.all()
    elif user.role == 'organizer':
        events = Event.query.filter_by(organizer_id=user.id).all()
    else:
        # Get events where user has passes
        passes = EventPass.query.filter_by(attendee_id=user.id).all()
        event_ids = [p.event_id for p in passes]
        events = Event.query.filter(Event.id.in_(event_ids)).all() if event_ids else []
    
    # Get user's passes
    my_passes = EventPass.query.filter_by(attendee_id=user.id).all()
    
    return render_template('dashboard.html', user=user, events=events, my_passes=my_passes)

@app.route('/browse-events')
@login_required
def browse_events():
    """View to see all available events created by all organizers"""
    events = Event.query.all()
    return render_template('browse_events.html', events=events)

@app.route('/create-event', methods=['GET', 'POST'])
@login_required
@role_required('organizer')
def create_event():
    if request.method == 'POST':
        name = request.form.get('name')
        date_str = request.form.get('date')
        venue = request.form.get('venue')
        details = request.form.get('details')
        
        user = User.query.get(session['user_id'])
        
        # Encrypt event details
        encrypted_details, encrypted_key = encrypt_data_hybrid(details, user.public_key)
        
        # Create event
        event = Event(
            name=name,
            date=datetime.strptime(date_str, '%Y-%m-%dT%H:%M'),
            venue=venue,
            organizer_id=user.id,
            encrypted_details=encrypted_details,
            encryption_key=encrypted_key
        )
        
        db.session.add(event)
        db.session.commit()
        
        # Grant organizer full permissions
        grant_permission(user.id, 'event', event.id, 'read')
        grant_permission(user.id, 'event', event.id, 'write')
        grant_permission(user.id, 'event', event.id, 'delete')
        grant_permission(user.id, 'event', event.id, 'validate')
        
        flash('Event created successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('create_event.html')

@app.route('/event/<int:event_id>')
@login_required
def view_event(event_id):
    event = Event.query.get_or_404(event_id)
    user = User.query.get(session['user_id'])
    
    # Check read permission
    has_permission = (
        user.role == 'admin' or 
        user.role == 'organizer' or 
        user.role == 'attendee' or 
        event.organizer_id == user.id or
        check_permission(user.id, 'event', event_id, 'read')
    )
    
    if not has_permission:
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    # Decrypt event details if organizer
    decrypted_details = None
    if event.organizer_id == user.id:
        try:
            decrypted_details = decrypt_data_hybrid(
                event.encrypted_details,
                event.encryption_key,
                user.private_key
            )
        except:
            decrypted_details = "Unable to decrypt"
    
    passes = EventPass.query.filter_by(event_id=event_id).all()
    
    return render_template('view_event.html', event=event, passes=passes, decrypted_details=decrypted_details)

@app.route('/generate-pass/<int:event_id>', methods=['POST'])
@login_required
def generate_pass(event_id):
    event = Event.query.get_or_404(event_id)
    user = User.query.get(session['user_id'])
    
    # Check if user already has a pass
    existing_pass = EventPass.query.filter_by(event_id=event_id, attendee_id=user.id).first()
    if existing_pass:
        flash('You already have a pass for this event', 'warning')
        return redirect(url_for('view_event', event_id=event_id))
    
    # Generate unique pass code
    pass_code = f"EVT{event_id:04d}ATT{user.id:04d}{secrets.token_hex(4).upper()}"
    
    # Create pass data for QR code
    pass_data = {
        'pass_code': pass_code,
        'event_id': event_id,
        'event_name': event.name,
        'attendee': user.username,
        'date': event.date.strftime('%Y-%m-%d %H:%M')
    }
    
    # Generate QR code
    qr_code = generate_qr_code(json.dumps(pass_data))
    
    # Create digital signature
    signature = create_digital_signature(pass_code, user.private_key)
    
    # Create pass
    event_pass = EventPass(
        pass_code=pass_code,
        event_id=event_id,
        attendee_id=user.id,
        qr_code=qr_code,
        digital_signature=signature
    )
    
    db.session.add(event_pass)
    db.session.commit()
    
    # Grant user read permission for this event
    if not check_permission(user.id, 'event', event_id, 'read'):
        grant_permission(user.id, 'event', event_id, 'read')
    
    flash('Event pass generated successfully!', 'success')
    return redirect(url_for('view_pass', pass_id=event_pass.id))

@app.route('/pass/<int:pass_id>')
@login_required
def view_pass(pass_id):
    event_pass = EventPass.query.get_or_404(pass_id)
    user = User.query.get(session['user_id'])
    
    # Check permission
    if event_pass.attendee_id != user.id and user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    event = Event.query.get(event_pass.event_id)
    attendee = User.query.get(event_pass.attendee_id)
    
    # Verify signature
    signature_valid = verify_digital_signature(
        event_pass.pass_code,
        event_pass.digital_signature,
        attendee.public_key
    )
    
    return render_template('view_pass.html', 
                         event_pass=event_pass, 
                         event=event, 
                         attendee=attendee,
                         signature_valid=signature_valid)

@app.route('/validate-pass', methods=['GET', 'POST'])
@login_required
def validate_pass():
    user = User.query.get(session['user_id'])
    
    if request.method == 'POST':
        pass_code = request.form.get('pass_code')
        
        event_pass = EventPass.query.filter_by(pass_code=pass_code).first()
        
        if not event_pass:
            flash('Invalid pass code', 'error')
            return redirect(url_for('validate_pass'))
        
        event = Event.query.get(event_pass.event_id)
        
        # Check validation permission
        has_permission = (
            user.role == 'admin' or
            event.organizer_id == user.id or
            check_permission(user.id, 'event', event.id, 'validate')
        )
        
        if not has_permission:
            flash('You do not have permission to validate passes for this event', 'error')
            return redirect(url_for('validate_pass'))
        
        # Verify digital signature
        attendee = User.query.get(event_pass.attendee_id)
        signature_valid = verify_digital_signature(
            event_pass.pass_code,
            event_pass.digital_signature,
            attendee.public_key
        )
        
        if not signature_valid:
            flash('Pass signature is invalid! Possible forgery detected.', 'error')
            return redirect(url_for('validate_pass'))
        
        if event_pass.is_used:
            flash(f'Pass already used on {event_pass.validated_at.strftime("%Y-%m-%d %H:%M")}', 'warning')
        else:
            event_pass.is_used = True
            event_pass.validated_at = datetime.utcnow()
            db.session.commit()
            flash('Pass validated successfully!', 'success')
        
        return render_template('validation_result.html', event_pass=event_pass, event=event, attendee=attendee)
    
    return render_template('validate_pass.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('index'))

# ============= INITIALIZE DATABASE =============

@app.before_request
def create_tables():
    """Create database tables before first request"""
    if not hasattr(app, 'tables_created'):
        db.create_all()
        app.tables_created = True

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
