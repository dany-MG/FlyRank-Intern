from fastapi import APIRouter, Depends, status
from src.middleware.auth_bearer import get_curr_user

router = APIRouter(tags=["Users"])

@router.get("/public/info", status_code= status.HTTP_200_OK)
def public_info():
    return {"message": "Welcome stranger! This info is public."}

@router.get("/protected/profile", status_code=status.HTTP_200_OK)
def get_protected_profile(current_user  = Depends(get_curr_user)):
    return {
        "message" : f"Welcome {current_user.email}! This info is protected and requires authentication.",
        "user_id" : current_user.id,
        "user_email" : current_user.email,
        "account_created" : current_user.created_at
    }

@router.get("/protected/dashboard", status_code=status.HTTP_200_OK)
def get_protected_dashboard(user: str = Depends(get_curr_user)):
    return{
        "message" : f"Hi! {user.email}. This is your dashboard. You are authenticated and can access this protected route.",
        "user_id" : user.id,
        "user_email" : user.email,
        "account_created" : user.created_at
    }

