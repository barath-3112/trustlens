from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from pymongo.errors import DuplicateKeyError
from .. import database
from ..deps import current_user
from ..schemas import RegisterRequest, LoginRequest, TokenResponse, UserResponse
from ..security import hash_password, verify_password, create_token

router = APIRouter(prefix="/api/auth", tags=["authentication"])
def present(user): return UserResponse(id=str(user["_id"]), name=user["name"], email=user["email"], created_at=user["created_at"])
@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(body: RegisterRequest):
    user={"name":body.name.strip(),"email":str(body.email).lower(),"password_hash":hash_password(body.password),"created_at":datetime.now(timezone.utc)}
    try: result=await database.database.users.insert_one(user)
    except DuplicateKeyError: raise HTTPException(400,"An account with this email already exists")
    user["_id"]=result.inserted_id
    return TokenResponse(access_token=create_token(str(result.inserted_id)),user=present(user))
@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest):
    user=await database.database.users.find_one({"email":str(body.email).lower()})
    if not user or not verify_password(body.password,user["password_hash"]): raise HTTPException(401,"Invalid email or password")
    return TokenResponse(access_token=create_token(str(user["_id"])),user=present(user))
@router.get("/me", response_model=UserResponse)
async def me(user=Depends(current_user)): return present(user)
