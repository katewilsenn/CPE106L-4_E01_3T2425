from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
from backend.models import EcoAction, eco_actions
from backend.database import get_db_connection

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
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user.username, user.password))
        conn.commit()
        conn.close()  # Close the connection after use
        return {"message": "✅ Registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail="❌ User already exists or error occurred")

@router.post("/login")
def login(user: UserLogin):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (user.username, user.password))
    result = cursor.fetchone()
    conn.close()  # Close the connection after use
    if result:
        return {"message": "✅ Login successful"}
    else:
        raise HTTPException(status_code=401, detail="❌ Invalid username or password")

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

# Register the router with the app
app.include_router(router)
