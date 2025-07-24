from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
from backend.database import get_db_connection
from typing import Optional
from datetime import datetime
from passlib.context import CryptContext
import sqlite3
from backend.database import get_db_connection

# Initialize password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()  # Define FastAPI app instance
router = APIRouter()

class EcoActionCreate(BaseModel):
    action: str
    points: int

class UserSignup(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class LogRequest(BaseModel):
    user: str
    action_id: int

class AdminLogin(BaseModel):
    username: str
    password: str

class ResetRequest(BaseModel):
    timeframe: str  # "month" or "year"
    
class MessageRequest(BaseModel):
    username: str
    message: str

# Add admin user check (you might want to store admin status in users table)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"  # In production, use environment variables

@router.get("/actions")
def get_actions():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, action, points FROM actions")
        actions = [{"id": row[0], "action": row[1], "points": row[2]} for row in cursor.fetchall()]
        conn.close()
        return actions
    except Exception as e:
        raise HTTPException(status_code=500, detail="❌ Failed to retrieve actions")

@router.post("/signup")
def signup(user: UserSignup):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Hash the password before storing
        hashed_password = pwd_context.hash(user.password)
        
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)", 
            (user.username, hashed_password)
        )
        conn.commit()
        return {"message": "✅ Registered successfully"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Username already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@router.post("/login")
def login(user: UserLogin):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT id, password_hash FROM users WHERE username=?", 
        (user.username,)
    )
    user_data = cursor.fetchone()
    
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_id, hashed_password = user_data
    if not pwd_context.verify(user.password, hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    
    return {"message": "✅ Login successful", "user_id": user_id}

@router.post("/log-action")
def log_action(req: LogRequest):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get action details
        cursor.execute("SELECT action, points FROM actions WHERE id = ?", (req.action_id,))
        action = cursor.fetchone()
        
        if not action:
            raise HTTPException(status_code=404, detail="Action not found")
        
        action_name, points = action
        
        # Get user ID
        cursor.execute("SELECT id FROM users WHERE username = ?", (req.user,))
        user = cursor.fetchone()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        user_id = user[0]
        
        # Insert log and get timestamp
        cursor.execute("""
            INSERT INTO logs (user_id, action_id, points)
            VALUES (?, ?, ?)
        """, (user_id, req.action_id, points))
        
        # Get the newly created log entry with timestamp
        cursor.execute("""
            SELECT l.timestamp 
            FROM logs l
            WHERE l.id = last_insert_rowid()
        """)
        timestamp = cursor.fetchone()[0]
        
        conn.commit()
        return {
            "message": f"✅ Logged: {action_name} (+{points} pts)",
            "timestamp": timestamp
        }
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error logging action: {str(e)}")
    finally:
        conn.close()

@router.get("/history/{username}")
def get_user_history(username: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT action, points, timestamp 
        FROM logs 
        WHERE username=? 
        ORDER BY timestamp DESC
    """, (username,))
    history = cursor.fetchall()
    conn.close()
    return history

@router.get("/user-points/{username}")
def get_total_points(username: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT SUM(l.points)
            FROM logs l
            JOIN users u ON l.user_id = u.id
            WHERE u.username = ?
        """, (username,))
        total = cursor.fetchone()[0] or 0
        return {"points": total}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@router.get("/leaderboard")
def get_leaderboard():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT u.username, SUM(l.points) as total_points
            FROM users u
            JOIN logs l ON u.id = l.user_id
            GROUP BY u.username
            ORDER BY total_points DESC
            LIMIT 10
        """)
        result = cursor.fetchall()
        return [{"username": row[0], "points": row[1] or 0} for row in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@router.get("/debug-users")
def debug_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

@router.post("/admin/login")
def admin_login(admin: AdminLogin):
    if admin.username == ADMIN_USERNAME and admin.password == ADMIN_PASSWORD:
        return {"message": "✅ Admin login successful"}
    raise HTTPException(status_code=401, detail="❌ Invalid admin credentials")

@router.post("/admin/reset-leaderboard")
def reset_leaderboard(req: ResetRequest):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if req.timeframe == "month":
            cursor.execute("DELETE FROM logs WHERE timestamp >= date('now', 'start of month')")
        elif req.timeframe == "year":
            cursor.execute("DELETE FROM logs WHERE timestamp >= date('now', 'start of year')")
        else:
            raise HTTPException(status_code=400, detail="Invalid timeframe")
            
        conn.commit()
        return {"message": f"✅ Leaderboard reset for {req.timeframe}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error resetting leaderboard: {str(e)}")
    finally:
        conn.close()

@router.post("/admin/send-congrats")
def send_congrats(req: MessageRequest):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Insert certificate into database
        cursor.execute(
            "INSERT INTO certificates (username, message) VALUES (?, ?)",
            (req.username, req.message)
        )
        
        conn.commit()
        return {"message": f"✅ Certificate sent to {req.username}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending certificate: {str(e)}")
    finally:
        conn.close()
        
@router.get("/admin/get-messages/{username}")
def get_messages(username: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT message FROM messages WHERE username=? AND is_read=0",
        (username,)
    )
    messages = [row[0] for row in cursor.fetchall()]
    
    # Mark messages as read
    cursor.execute(
        "UPDATE messages SET is_read=1 WHERE username=?",
        (username,)
    )
    conn.commit()
    conn.close()
    return {"messages": messages}

@router.post("/admin/add-action")
def add_eco_action(action: EcoActionCreate):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if action already exists
        cursor.execute("SELECT id FROM actions WHERE action=?", (action.action,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Action already exists")
            
        cursor.execute(
            "INSERT INTO actions (action, points) VALUES (?, ?)",
            (action.action, action.points)
        )
        conn.commit()
        return {"message": f"✅ Added new action: {action.action} ({action.points} pts)"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding action: {str(e)}")
    finally:
        conn.close()

@router.get("/user-history/{username}")
def get_user_history(username: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT l.id, a.action, l.points, l.timestamp 
            FROM logs l
            JOIN actions a ON l.action_id = a.id
            JOIN users u ON l.user_id = u.id
            WHERE u.username = ?
            ORDER BY l.timestamp DESC
        """, (username,))
        history = cursor.fetchall()
        return [{
            "id": row[0],
            "action": row[1],
            "points": row[2],
            "timestamp": row[3]
        } for row in history]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

# Register the router with the app
app.include_router(router)