import sqlite3
import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

DB_PATH = os.path.join(os.path.dirname(__file__), "vibecode.db")

# --- Security & AES-256-GCM Encryption Module ---

def derive_key(passphrase: str, salt: bytes) -> bytes:
    """Derive a 256-bit AES key from a passphrase using PBKDF2HMAC-SHA256."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000
    )
    return kdf.derive(passphrase.encode())

def encrypt_data(passphrase: str, plaintext: str) -> str:
    """Encrypt plaintext using AES-256-GCM with a PBKDF2-derived key."""
    if not plaintext:
        return ""
    salt = os.urandom(16)
    nonce = os.urandom(12)
    key = derive_key(passphrase, salt)
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode("utf-8"), None)
    
    # Store as: Salt (16 bytes) + Nonce (12 bytes) + Ciphertext
    combined = salt + nonce + ciphertext
    return base64.b64encode(combined).decode("utf-8")

def decrypt_data(passphrase: str, encrypted_base64: str) -> str:
    """Decrypt base64-encoded ciphertext using AES-256-GCM."""
    if not encrypted_base64:
        return ""
    try:
        combined = base64.b64decode(encrypted_base64.encode("utf-8"))
        if len(combined) < 28:
            raise ValueError("Ciphertext too short.")
        
        salt = combined[:16]
        nonce = combined[16:28]
        ciphertext = combined[28:]
        
        key = derive_key(passphrase, salt)
        aesgcm = AESGCM(key)
        decrypted = aesgcm.decrypt(nonce, ciphertext, None)
        return decrypted.decode("utf-8")
    except Exception as e:
        raise ValueError("Decryption failed. Invalid passcode or corrupted data.") from e

# --- SQLite Database Module ---

def get_db_connection():
    """Establish connection to SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database tables."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Vault Table: Stores encrypted student profiles and grades
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_vault (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            encrypted_profile TEXT,
            encrypted_grades TEXT,
            is_locked INTEGER DEFAULT 1
        )
    """)
    
    # Benchmark Table: Stores performance metrics for algorithms
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS benchmarks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            algorithm TEXT,
            num_operations INTEGER,
            time_taken_ms REAL,
            complexity_estimate TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Challenges Table: Stores student study scores and completion status
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS challenges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            challenge_name TEXT UNIQUE,
            status TEXT DEFAULT 'Not Started',
            score INTEGER DEFAULT 0,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Seed standard challenges if empty
    cursor.execute("SELECT COUNT(*) FROM challenges")
    if cursor.fetchone()[0] == 0:
        challenges = [
            ("Binary Search Tree Basics", "In Progress", 0),
            ("AVL Tree Rebalancing", "Not Started", 0),
            ("Graph BFS Traversal", "Not Started", 0),
            ("Quick Sort Partitioning", "Not Started", 0)
        ]
        cursor.executemany(
            "INSERT INTO challenges (challenge_name, status, score) VALUES (?, ?, ?)",
            challenges
        )
        
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
