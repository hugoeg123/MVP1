from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from ..auth.jwt import create_access_token, get_current_user
from ..core.config import settings
from ..models.user import User, UserCreate
from ..db.session import get_db
from ..auth.security import authenticate_user

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    refresh_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/register", response_model=User)
async def register(user: UserCreate):
    # Here you would typically create a new user in your database
    # For demo purposes, we'll return a mock user
    return {
        "id": 1,
        "email": user.email,
        "full_name": user.full_name,
        "is_active": True,
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    }

@router.get("/me", response_model=User)
async def read_users_me(current_user: str = Depends(get_current_user)):
    # Here you would typically query your database to get the user details
    # For demo purposes, we'll return a mock user
    return {
        "id": 1,
        "email": current_user,
        "full_name": "Demo User",
        "is_active": True,
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    }