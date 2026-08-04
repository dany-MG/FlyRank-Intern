from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.services.auth_service import AuthService

security = HTTPBearer()

def get_token(credentials : HTTPAuthorizationCredentials = Depends(security)):
    return credentials.credentials

def get_curr_user(token: str = Depends(get_token)):
    try:
        res = AuthService.get_user(token)
        return res.user
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

