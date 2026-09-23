from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from .config import get_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(password: str) -> str: return pwd_context.hash(password)
def verify_password(password: str, hashed: str) -> bool: return pwd_context.verify(password, hashed)
def create_token(subject: str) -> str:
    cfg = get_settings(); expires = datetime.now(timezone.utc) + timedelta(minutes=cfg.access_token_expire_minutes)
    return jwt.encode({"sub": subject, "exp": expires}, cfg.jwt_secret, algorithm=cfg.jwt_algorithm)
def decode_token(token: str) -> str | None:
    try: return jwt.decode(token, get_settings().jwt_secret, algorithms=[get_settings().jwt_algorithm]).get("sub")
    except JWTError: return None
