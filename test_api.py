# test_api.py
import requests
import json

# Základní URL adresa našeho API
BASE_URL = "http://127.0.0.1:8000/api/tasks/"

# --- Krok 1: Vytvoření nového úkolu (POST) ---
print("Vytvářím nový úkol...")
new_task_data = {
    "title": "Naučit se Django a FastAPI",
    "description": "Spojit robustnost Django a rychlost FastAPI."
}
response = requests.post(BASE_URL, json=new_task_data)
created_task = response.json()
print(f"Úkol byl vytvořen: {created_task}")
print("-" * 30)

# --- Krok 2: Získání všech úkolů (GET) ---
print("Získávám všechny úkoly...")
response = requests.get(BASE_URL)
all_tasks = response.json()
print("Všechny úkoly:")
# Použijeme 'json.dumps' pro hezčí výpis
print(json.dumps(all_tasks, indent=4))
print("-" * 30)

# --- Krok 3: Aktualizace úkolu (PUT) ---
# Použijeme ID úkolu, který jsme právě vytvořili
task_id_to_update = created_task['id']
print(f"Aktualizuji úkol s ID {task_id_to_update}...")
updated_task_data = {
    "title": "Ovládnout Django a FastAPI",
    "description": "Popis byl upraven."
}
response = requests.put(f"{BASE_URL}{task_id_to_update}", json=updated_task_data)
updated_task = response.json()
print(f"Úkol byl aktualizován: {updated_task}")
print("-" * 30)

# --- Krok 4: Smazání úkolu (DELETE) ---
print(f"Mažu úkol s ID {task_id_to_update}...")
response = requests.delete(f"{BASE_URL}{task_id_to_update}")
print(f"Stavový kód smazání: {response.status_code}")
print("Úkol byl smazán.")
print("-" * 30)

# --- Krok 5: Ověření smazání (GET) ---
print("Ověřuji smazání (získávám úkoly znovu)...")
response = requests.get(BASE_URL)
remaining_tasks = response.json()
print("Zbývající úkoly:")
print(remaining_tasks)