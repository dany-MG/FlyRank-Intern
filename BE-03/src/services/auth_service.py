from src.database.supabase import supabase
from pydantic import EmailStr

class AuthService:
    @staticmethod
    def sign_up(email: EmailStr, password: str):
        return supabase.auth.sign_up({
            "email": email,
            "password": password
        })

    @staticmethod
    def  login(email:EmailStr, password:str):
        return supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
    
