import os
import requests
from dotenv import load_dotenv

# Lade die Passwörter aus der .env Datei
load_dotenv()

HA_URL = os.getenv("HA_URL", "http://localhost:8123")
HA_TOKEN = os.getenv("HA_TOKEN")

def ha_control(entity_id: str, command: str):
    """
    Sendet einen echten Befehl an Home Assistant.
    """
    if not HA_TOKEN:
        return "[ERROR] Kein Home Assistant Token in .env gefunden!"

    # Wir bauen die URL für den Befehl (Service Call)
    # Beispiel: http://localhost:8123/api/services/light/turn_on
    domain = entity_id.split(".")[0]  # z.B. "light" aus "light.wohnzimmer"
    url = f"{HA_URL}/api/services/{domain}/{command}"
    
    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "content-type": "application/json",
    }
    data = {"entity_id": entity_id}

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return f"[HOME ASSISTANT] Erfolgreich: {command} an {entity_id} gesendet."
        else:
            return f"[ERROR] Home Assistant antwortet: {response.status_code} - {response.text}"
    except Exception as e:
        return f"[ERROR] Verbindung fehlgeschlagen: {e}"

# --- REGISTER ---
AVAILABLE_TOOLS = {
    "ha_control": ha_control
}

def execute_tool(tool_name: str, **kwargs):
    if tool_name in AVAILABLE_TOOLS:
        return AVAILABLE_TOOLS[tool_name](**kwargs)
    return f"[SYSTEM] Tool '{tool_name}' nicht gefunden."