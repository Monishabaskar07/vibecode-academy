import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

# Import local modules
from database import init_db, get_db_connection, encrypt_data, decrypt_data
from agents.coordinator import LearningCoordinatorAgent
from mcp.server import run_benchmark

app = FastAPI(title="VibeCode Academy API", version="1.0.0")

# Enable CORS for local Vite development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In development, allow Vite client on 5173
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_db()

coordinator = LearningCoordinatorAgent()

# --- Pydantic Data Models ---

class SessionRequest(BaseModel):
    prompt: str
    eli5_mode: bool = False

class VaultUnlockRequest(BaseModel):
    passcode: str

class VaultSaveRequest(BaseModel):
    passcode: str
    student_name: str
    grade_level: str
    homework_notes: str
    grades_summary: str

class BenchmarkRequest(BaseModel):
    algorithm: str
    num_operations: int

class ChallengeUpdateRequest(BaseModel):
    challenge_name: str
    status: str
    score: int

# --- API Endpoints ---

@app.post("/api/session")
def run_session(req: SessionRequest):
    """Run the multi-agent algorithm playground pipeline."""
    try:
        payload = coordinator.process_session(req.prompt, req.eli5_mode)
        return payload
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent pipeline failure: {str(e)}")

@app.get("/api/vault/status")
def get_vault_status():
    """Check if the student vault is locked and if any profile exists."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT is_locked, encrypted_profile FROM student_vault LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return {"exists": False, "is_locked": True}
    return {
        "exists": True, 
        "is_locked": bool(row["is_locked"]),
        "encrypted_data_preview": row["encrypted_profile"][:60] + "..." if row["encrypted_profile"] else ""
    }

@app.post("/api/vault/save")
def save_vault(req: VaultSaveRequest):
    """Encrypt and save student profile and grades using AES-256-GCM."""
    try:
        # Construct plain text payloads
        profile_text = f"Name: {req.student_name} | Grade: {req.grade_level} | Notes: {req.homework_notes}"
        grades_text = req.grades_summary
        
        # Encrypt locally using passphrase
        enc_profile = encrypt_data(req.passcode, profile_text)
        enc_grades = encrypt_data(req.passcode, grades_text)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Clear existing and insert new (single-student local vault)
        cursor.execute("DELETE FROM student_vault")
        cursor.execute(
            "INSERT INTO student_vault (username, encrypted_profile, encrypted_grades, is_locked) VALUES (?, ?, ?, 1)",
            ("student", enc_profile, enc_grades)
        )
        conn.commit()
        conn.close()
        return {"message": "Student profile securely encrypted and stored."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/vault/unlock")
def unlock_vault(req: VaultUnlockRequest):
    """Attempt to decrypt the student vault using the passphrase."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT encrypted_profile, encrypted_grades FROM student_vault LIMIT 1")
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="No profile found in vault. Please save a profile first.")
        
    try:
        # Cryptographic Decryption
        dec_profile = decrypt_data(req.passcode, row["encrypted_profile"])
        dec_grades = decrypt_data(req.passcode, row["encrypted_grades"])
        
        # Mark as unlocked in database (session-based, but we persist status)
        cursor.execute("UPDATE student_vault SET is_locked = 0 WHERE username = 'student'")
        conn.commit()
        conn.close()
        
        return {
            "is_locked": False,
            "profile": dec_profile,
            "grades": dec_grades
        }
    except ValueError as e:
        conn.close()
        # Explicit cryptographic decryption failure
        raise HTTPException(status_code=400, detail="Cryptographic Decryption Failed! Invalid Vault Passcode.")
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/vault/lock")
def lock_vault():
    """Re-lock the student vault."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE student_vault SET is_locked = 1 WHERE username = 'student'")
    conn.commit()
    conn.close()
    return {"is_locked": True}

@app.get("/api/benchmarks")
def get_benchmarks():
    """List recent performance benchmarks."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT algorithm, num_operations, time_taken_ms, complexity_estimate, timestamp FROM benchmarks ORDER BY id DESC LIMIT 10")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.post("/api/benchmarks/run")
def trigger_benchmark(req: BenchmarkRequest):
    """Run a high-speed simulation using MCP tool logic and log the metrics."""
    try:
        # Run standard local benchmark (matching MCP server functionality)
        time_taken = run_benchmark(req.algorithm, req.num_operations)
        
        # Estimate Big-O complexity signature based on scaling rules
        if req.algorithm in ["bst", "avl"]:
            complexity = "O(log N)"
        elif req.algorithm == "quicksort":
            complexity = "O(N log N)"
        else:
            complexity = "O(N)"
            
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO benchmarks (algorithm, num_operations, time_taken_ms, complexity_estimate) VALUES (?, ?, ?, ?)",
            (req.algorithm, req.num_operations, time_taken, complexity)
        )
        conn.commit()
        conn.close()
        
        return {
            "algorithm": req.algorithm,
            "num_operations": req.num_operations,
            "time_taken_ms": time_taken,
            "complexity": complexity
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/challenges")
def get_challenges():
    """List student challenges and scores."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT challenge_name, status, score FROM challenges")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.post("/api/challenges/update")
def update_challenge(req: ChallengeUpdateRequest):
    """Update challenge score and status."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE challenges SET status = ?, score = ? WHERE challenge_name = ?",
        (req.status, req.score, req.challenge_name)
    )
    conn.commit()
    conn.close()
    return {"message": f"Challenge '{req.challenge_name}' updated successfully."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
