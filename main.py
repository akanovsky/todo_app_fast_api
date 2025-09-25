# main.py
import os
import django
from fastapi import FastAPI

# 1. Nejdříve nastavíme prostředí Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

# 2. Až poté importujeme routery, které používají Django modely
from api import routers
# from .api import auth_router

# 3. Vytvoříme a nastavíme aplikaci FastAPI
app = FastAPI()

# app.include_router(auth_router.router, prefix="/api")
app.include_router(routers.router, prefix="/api")