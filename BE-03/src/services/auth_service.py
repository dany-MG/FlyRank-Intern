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
    def login(email:EmailStr, password:str):
        return supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

    @staticmethod
    def get_user(token: str):
        return supabase.auth.get_user(token)

    @staticmethod
    def logout(token: str):
        supabase.auth.set_session(token, "")
        return supabase.auth.sign_out()
    
    
