from fastapi import APIRouter
from pydantic import BaseModel
from backend.models import EcoAction, eco_actions
from backend.database import conn

router = APIRouter()
cursor = conn.cursor()

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
    cursor = conn.cursor()
    cursor.execute("SELECT id, action, points FROM actions")
    actions = [{"id": row[0], "action": row[1], "points": row[2]} for row in cursor.ftetchall()]
  return eco_action

@router.post("/signup")
def signup(user: UserSignup):
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user.username, user.password))
        conn.commit()
        return {"message": "✅ Registered successfully"}
    except Exception as e:
        return {"detail": "❌ User already exists or error occurred"}

@router.post("/login")
def login(user: UserLogin):
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (user.username, user.password))
    result = cursor.fetchone()
    if result:
        return {"message": "✅ Login successful"}
    else:
        return {"detail": "❌ Invalid username or password"}

@router.post("/log-action")
def log_action(req: LogRequest):
    matching = [a for a in eco_actions if a.id == req.action_id]
    if not matching:
        return {"error": "Invalid action ID"}
    action = matching[0]
    cursor.execute("INSERT INTO logs (username, action, points) VALUES (?, ?, ?)", (req.user, action.action, action.points))
    conn.commit()
    return {"message": f"✅ Logged: {action.action} (+{action.points} pts)"}

@router.get("/history/{username}")
def get_user_history(username: str):
    cursor.execute("SELECT action, points FROM logs WHERE username=? ORDER BY timestamp DESC", (username,))
    return cursor.fetchall()
