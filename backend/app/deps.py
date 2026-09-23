from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from bson import ObjectId
from . import database
from .security import decode_token

bearer = HTTPBearer(auto_error=False)
async def current_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer)):
    if not credentials or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    subject = decode_token(credentials.credentials)
    if not subject or not ObjectId.is_valid(subject) or database.database is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    user = await database.database.users.find_one({"_id": ObjectId(subject)})
    if not user: raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    return user
