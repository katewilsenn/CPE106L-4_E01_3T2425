from fastapi import FastAPI
from backend.router import router

app = FastAPI()
app.include_router(router)

# Add this if you want to run directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
