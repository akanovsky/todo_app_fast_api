# main.py
from dotenv import load_dotenv
load_dotenv()

import os
import sys
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# Nastav cestu k Django projektu
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import django
django.setup()

# Importuj Django a FastAPI aplikace
from config.wsgi import application as django_application
from api.routers import router as api_router

# Vytvoř instanci FastAPI
app = FastAPI()

# Nastav CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Připoj API router pod cestou /api. Je důležité, aby bylo nahoře!
app.include_router(api_router, prefix="/api")

# Připoj statické soubory
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")),
    name="static"
)

# Na hlavní cestu připoj celou Django aplikaci
app.mount("/", WSGIMiddleware(django_application))