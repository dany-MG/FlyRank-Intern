from fastapi import APIRouter, Header, HTTPException, status

router = APIRouter(tags=["Users"])

@router.get("/public/info", status_code= status.HTTP_200_OK)
def public_info():
    return {"message": "Welcome stranger! This info is public."}

@router.get("/protected/profile", status_code=status.HTTP_200_OK)
def get_protected_profile(authorization: str = Header(default=None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token required")

    token = authorization.split(" ")[1]

    return {
        "message" : "Token captured!", 
        "token_received" : token
    }

