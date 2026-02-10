import time
import sys
import json
from skills.registry import execute_tool

# Konfiguration: Herzschlag (Wie oft Nuri aufwacht)
HEARTBEAT_RATE = 5 

def main():
    print("---------------------------------------")
    print("NURI SYSTEM START - MODE: AUTONOMOUS")
    print("---------------------------------------")
    
    while True:
        try:
            print(f"\n[Nuri] Scanne Umgebung... (Warte auf Input)")
            
            # --- 1. SIMULATION (Das Gehirn) ---
            # Aktuell tun wir so, als hätte die KI entschieden, das Licht anzumachen.
            # Später ersetzen wir das durch: response = ollama.chat(...)
            
            simulated_intent = {
                "tool": "ha_control",
                "params": {
                    "entity_id": "light.living_room",
                    "command": "turn_on"
                }
            }
            
            print(f"[THOUGHT] KI entscheidet: Nutze Tool '{simulated_intent['tool']}'")
            
            # --- 2. EXECUTION (Die Hand) ---
            # Hier wird der Befehl an die registry.py übergeben
            result = execute_tool(
                tool_name=simulated_intent['tool'], 
                **simulated_intent['params']
            )
            
            print(f"[ACTION RESULT] {result}")
            
            # --- 3. SLEEP ---
            time.sleep(HEARTBEAT_RATE)
            
        except KeyboardInterrupt:
            print("\n[Nuri] Shutdown initiiert. Gute Nacht.")
            sys.exit(0)
        except Exception as e:
            print(f"[ERROR] Kritischer Fehler im Loop: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()