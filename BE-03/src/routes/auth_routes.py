from fastapi import APIRouter, HTTPException, status, Depends
from src.schemas.auth_schema import AuthSchema
from src.services.auth_service import AuthService
from src.middleware.auth_bearer import get_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(req: AuthSchema):
    if not req.usr_email or not req.usr_pass:
        raise HTTPException(status_code=400, detail= "Email and password are required")

    try:
        res = AuthService.sign_up(req.usr_email, req.usr_pass)
        return res.user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", status_code=status.HTTP_200_OK)
def login(req: AuthSchema):
    if not req.usr_email or not req.usr_pass:
        raise HTTPException(status_code=400, detail= "Email and password are required")

    try:
        res = AuthService.login(req.usr_email, req.usr_pass)
        return {
            "access_token" : res.session.access_token,
            "refresh_token" : res.session.refresh_token,
        }
    except Exception as e:
        raise HTTPException(status_code =401, detail="Invalid login credentials")

@router.post("/logout", status_code = status.HTTP_204_NO_CONTENT)
def logout(token: str = Depends(get_token)):
    try:
        AuthService.logout(token)
        return {"message": "Successfully logged out"}
    except Exception:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail = "Error loging out or token already invalid")


    
