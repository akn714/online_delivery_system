"""Authentication routes for user signup and login."""
from fastapi import APIRouter, HTTPException
from datetime import datetime
import hashlib
import uuid
import random
import string
import bcrypt

from models.order import UserCreate, UserLogin, UserResponse, TokenResponse
from database.supabase_client import get_supabase

router = APIRouter(prefix="/api/auth", tags=["authentication"])

def generate_user_id() -> str:
    """Generate a unique user ID."""
    return f"USR#{uuid.uuid4().hex[:8].upper()}"


def _prepare_password(password: str) -> bytes:
    """
    Normalize password before bcrypt hashing.

    Bcrypt only supports up to 72 bytes of input. We pre-hash with SHA-256 to
    avoid runtime failures for longer/multibyte passwords and keep behavior consistent.
    """
    return hashlib.sha256(password.encode("utf-8")).hexdigest().encode("utf-8")


def hash_password(password: str) -> str:
    """Hash a password using bcrypt with safe input normalization."""
    prepared = _prepare_password(password)
    return bcrypt.hashpw(prepared, bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify password against stored hash.

    First verify using the normalized flow. If that fails, attempt legacy direct
    bcrypt verification for previously created accounts.
    """
    stored_hash = hashed_password.encode("utf-8")

    # Preferred verification path for new hashes created via _prepare_password.
    try:
        if bcrypt.checkpw(_prepare_password(plain_password), stored_hash):
            return True
    except ValueError:
        return False

    # Backward compatibility for earlier bcrypt hashes that used raw password bytes.
    raw_password = plain_password.encode("utf-8")
    if len(raw_password) > 72:
        return False

    try:
        return bcrypt.checkpw(raw_password, stored_hash)
    except ValueError:
        return False


def generate_token() -> str:
    """Generate a simple access token."""
    return f"tok_{uuid.uuid4().hex}{random.choice(string.ascii_letters)}"


@router.post("/signup", response_model=TokenResponse)
async def signup(user_data: UserCreate):
    """
    Register a new user.
    """
    supabase = get_supabase()
    
    # Check if phone number already exists
    existing_user = supabase.table("users").select("*").eq("phone", user_data.phone).execute()
    
    if existing_user.data and len(existing_user.data) > 0:
        raise HTTPException(status_code=400, detail="Phone number already registered")
    
    # Hash the password
    hashed_password = hash_password(user_data.password)
    
    # Generate user ID
    user_id = generate_user_id()
    
    # Create user record
    user_record = {
        "id": user_id,
        "name": user_data.name,
        "phone": user_data.phone,
        "password": hashed_password,
        "created_at": datetime.now().isoformat()
    }
    
    # Insert into Supabase
    result = supabase.table("users").insert(user_record).execute()
    
    if result.data:
        user = result.data[0]
        # Generate access token
        access_token = generate_token()
        
        return TokenResponse(
            access_token=access_token,
            user=UserResponse(
                id=user["id"],
                name=user["name"],
                phone=user["phone"],
                created_at=user["created_at"]
            )
        )
    else:
        raise HTTPException(status_code=500, detail="Failed to create user")


@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    """
    Authenticate a user and return access token.
    """
    supabase = get_supabase()
    
    # Find user by phone
    result = supabase.table("users").select("*").eq("phone", credentials.phone).execute()
    
    if not result.data or len(result.data) == 0:
        raise HTTPException(status_code=401, detail="Invalid phone number or password")
    
    user = result.data[0]
    
    # Verify password
    if not verify_password(credentials.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid phone number or password")
    
    # Generate access token
    access_token = generate_token()
    
    return TokenResponse(
        access_token=access_token,
        user=UserResponse(
            id=user["id"],
            name=user["name"],
            phone=user["phone"],
            created_at=user["created_at"]
        )
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user(authorization: str):
    """
    Get current user details from token.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    token = authorization.replace("Bearer ", "")
    
    # In a real app, you'd decode the JWT token
    # For simplicity, we'll just return a placeholder
    # The token would be stored in localStorage on frontend
    
    supabase = get_supabase()
    
    # For now, we'll skip token validation and just return a mock response
    # In production, implement proper JWT validation
    raise HTTPException(status_code=401, detail="Invalid token")