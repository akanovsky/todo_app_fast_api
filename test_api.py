# test_api.py
import requests
import os
import django
from dotenv import load_dotenv

# Načti proměnné prostředí ze souboru .env
load_dotenv()

# Nastav Django prostředí
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

# Získej API klíč z .env souboru
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY not found in .env file")

# Nastav hlavičky s API klíčem pro všechny požadavky
headers = {
    "X-API-Key": API_KEY
}

# Základní URL adresa pro API
BASE_URL = "http://127.0.0.1:8000/api"

print("--- Testování GET požadavku (před vytvořením) ---")
response = requests.get(f"{BASE_URL}/tasks/", headers=headers)
print(f"Status kód: {response.status_code}")
print(f"Odpověď: {response.json()}\n")

print("--- Testování POST požadavku ---")
task_data = {
    "title": "Napsat testy API",
    "description": "Napsat integrační testy pro FastAPI API."
}
response = requests.post(f"{BASE_URL}/tasks/", json=task_data, headers=headers)
print(f"Status kód: {response.status_code}")
new_task = response.json()
print(f"Nový úkol: {new_task}\n")

if response.status_code == 200:
    new_task_id = new_task["id"]
    print(f"--- Testování PUT požadavku (úkol s ID {new_task_id}) ---")
    update_data = {
        "title": "Napsat testy API - Dokončeno",
        "completed": True
    }
    response = requests.put(f"{BASE_URL}/tasks/{new_task_id}", json=update_data, headers=headers)
    print(f"Status kód: {response.status_code}")
    print(f"Upravený úkol: {response.json()}\n")

    print(f"--- Testování GET požadavku (po vytvoření) ---")
    response = requests.get(f"{BASE_URL}/tasks/", headers=headers)
    print(f"Status kód: {response.status_code}")
    print(f"Odpověď: {response.json()}\n")

    print(f"--- Testování DELETE požadavku (úkol s ID {new_task_id}) ---")
    response = requests.delete(f"{BASE_URL}/tasks/{new_task_id}", headers=headers)
    print(f"Status kód: {response.status_code}")
    print("Úkol smazán.")

else:
    print("Nelze pokračovat v testování PUT a DELETE, POST požadavek selhal.")