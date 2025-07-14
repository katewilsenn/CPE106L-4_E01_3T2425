from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
from backend.models import EcoAction, eco_actions
from backend.database import get_db_connection
from backend import database  # or just import database if same directory

app = FastAPI()  # Define FastAPI app instance

router = APIRouter()

class UserSignup(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class LogRequest(BaseModel):
    user: str
    action_id: int

@router.get("/actions")
def get_actions():
    try:
        # Create a new database connection for this request
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, action, points FROM actions")
        actions = [{"id": row[0], "action": row[1], "points": row[2]} for row in cursor.fetchall()]
        conn.close()  # Close the connection after use
        return actions
    except Exception as e:
        raise HTTPException(status_code=500, detail="❌ Failed to retrieve actions")

@router.post("/signup")
def signup(user: UserSignup):
    try:
        conn = get_db_connection()  # If you're using per-request connection
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user.username, user.password))
        conn.commit()  # ✅ commit ensures data is saved
        cursor.close()
        conn.close()
        return {"message": "✅ Registered successfully"}
    except Exception as e:
        print("❌ Signup error:", e)
        raise HTTPException(status_code=400, detail="User may already exist.")

@router.post("/login")
def login(user: UserLogin):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username=?", (user.username,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="❌ User not found")

    stored_password = row[0]
    if stored_password != user.password:
        raise HTTPException(status_code=401, detail="❌ Incorrect password")

    return {"message": "✅ Login successful"}

@router.post("/log-action")
def log_action(req: LogRequest):
    matching = [a for a in eco_actions if a.id == req.action_id]
    if not matching:
        raise HTTPException(status_code=400, detail="❌ Invalid action ID")

    action = matching[0]
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs (username, action, points) VALUES (?, ?, ?)", (req.user, action.action, action.points))
    conn.commit()
    conn.close()  # Close the connection after use

    return {"message": f"✅ Logged: {action.action} (+{action.points} pts)"}

@router.get("/history/{username}")
def get_user_history(username: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT action, points FROM logs WHERE username=? ORDER BY timestamp DESC", (username,))
    history = cursor.fetchall()
    conn.close()  # Close the connection after use
    return history

@router.get("/user-points/{username}")
def get_total_points(username: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(points) FROM logs WHERE username=?", (username,))
    total = cursor.fetchone()[0] or 0
    conn.close()
    return {"points": total}

@router.get("/leaderboard")
def get_leaderboard():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username, SUM(points) as total_points FROM logs GROUP BY username ORDER BY total_points DESC LIMIT 10")
    result = cursor.fetchall()
    conn.close()
    return [{"username": row[0], "points": row[1]} for row in result]

@router.get("/debug-users")
def debug_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

# Register the router with the app
app.include_router(router)

