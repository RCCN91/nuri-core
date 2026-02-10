import datetime

# --- TEIL 1: Die Werkzeuge (Skills) ---

def ha_control(entity_id: str, command: str):
    """
    Simuliert die Steuerung von Home Assistant Geräten.
    Z.B. Licht an/aus, Heizung setzen.
    """
    # Später: Hier wird der echte WebSocket-Befehl an Home Assistant gesendet
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    return f"[{timestamp}] [HOME ASSISTANT] Befehl '{command}' an '{entity_id}' erfolgreich gesendet."

def calendar_add(title: str, date: str):
    """
    Simuliert das Eintragen eines Termins in den Google Kalender.
    Format Datum: YYYY-MM-DD
    """
    # Später: Hier kommt die Google Calendar API Logik hin
    return f"[GOOGLE CALENDAR] Termin '{title}' für das Datum {date} wurde erstellt."

def get_weather(location: str = "Zuhause"):
    """
    Simuliert eine Wetterabfrage.
    """
    # Später: Hier fragen wir OpenMeteo oder Home Assistant ab
    return f"[WETTER] In {location} sind es aktuell 18 Grad, leicht bewölkt."

# --- TEIL 2: Das Register (Die Mapping-Tabelle) ---

# Hier verknüpfen wir den "Text-Namen", den die KI nutzt, mit der echten Python-Funktion.
AVAILABLE_TOOLS = {
    "ha_control": ha_control,
    "calendar_add": calendar_add,
    "get_weather": get_weather
}

def execute_tool(tool_name: str, **kwargs):
    """
    Der 'Dispatcher'. Er nimmt den Wunschnamen der KI entgegen, sucht die Funktion
    und führt sie aus.
    """
    if tool_name in AVAILABLE_TOOLS:
        func = AVAILABLE_TOOLS[tool_name]
        try:
            # Wir rufen die Funktion mit den Parametern auf, die die KI geliefert hat
            return func(**kwargs)
        except Exception as e:
            return f"[ERROR] Fehler beim Ausführen von {tool_name}: {e}"
    else:
        return f"[SYSTEM] Fehler: Tool '{tool_name}' ist nicht bekannt."