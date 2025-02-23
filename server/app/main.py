from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.logging import log_middleware

app = FastAPI(
    title="Health MVP API",
    description="Backend API for the Health MVP application",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add logging middleware
app.middleware("http")(log_middleware)

@app.get("/")
async def root():
    return {"message": "Welcome to Health MVP API"}