# api/api_key_auth.py
from fastapi import Header, HTTPException, status, Depends
from dotenv import load_dotenv
import os
import sys
from asgiref.sync import sync_to_async

# Ujisti se, že importujeme Django modely
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

load_dotenv()

API_KEY = os.getenv("API_KEY")


async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Neplatný API klíč",
        )
    return True


async def get_current_user(key_verified: bool = Depends(verify_api_key)):
    try:
        from django.contrib.auth.models import User

        user = await sync_to_async(User.objects.first)()
        if not user:
            raise HTTPException(status_code=500, detail="V databázi není žádný uživatel. Vytvořte ho.")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chyba při získávání uživatele: {e}")