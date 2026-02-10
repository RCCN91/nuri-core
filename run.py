import sys
import json
import ollama
from skills.registry import execute_tool

# --- KONFIGURATION ---
MODEL = "llama3"  # Das Gehirn

# Das System-Prompt: Hier erklären wir Nuri, wer er ist und wie er antworten MUSS.
SYSTEM_PROMPT = """
Du bist Nuri, ein intelligenter KI-Assistent für das Smart Home.
Du hast Zugriff auf folgende Tools:
1. ha_control(entity_id, command): Steuert Geräte (command: 'turn_on' oder 'turn_off').

WICHTIG: Antworte IMMER im JSON-Format. Kein Text davor oder danach.
Wenn der User etwas will, das du steuern kannst, antworte so:
{
  "tool": "ha_control",
  "params": {
    "entity_id": "input_boolean.nuri_test",
    "command": "turn_on"
  }
}

Wenn du nicht helfen kannst oder nur reden sollst, antworte so:
{
  "tool": "chat",
  "response": "Hier deine Antwort..."
}

Aktuelle Geräte-Liste (Merke dir diese IDs):
- Licht/Testschalter: input_boolean.nuri_test
"""

def main():
    print(f"---------------------------------------")
    print(f"NURI SYSTEM ONLINE (Model: {MODEL})")
    print(f"---------------------------------------")
    
    while True:
        try:
            # 1. INPUT: Wir warten auf deine Eingabe
            user_input = input("\n[Du] Sag was: ")
            
            if user_input.lower() in ["exit", "quit", "aus"]:
                print("[Nuri] Fahre herunter...")
                break

            print(f"[Nuri] Denkt nach...")

            # 2. THINK: Anfrage an Ollama senden
            response = ollama.chat(model=MODEL, messages=[
                {'role': 'system', 'content': SYSTEM_PROMPT},
                {'role': 'user', 'content': user_input},
            ])
            
            ai_response_text = response['message']['content']
            
            # 3. PARSE: Versuchen, das JSON zu verstehen
            try:
                # Manchmal packt Llama das JSON in Markdown (```json ... ```), das entfernen wir
                clean_json = ai_response_text.replace("```json", "").replace("```", "").strip()
                intent = json.loads(clean_json)
                
                # 4. ACT: Entscheidung ausführen
                tool_name = intent.get("tool")
                
                if tool_name == "ha_control":
                    print(f"[THOUGHT] Ich schalte das Gerät...")
                    result = execute_tool(tool_name, **intent['params'])
                    print(f"[RESULT] {result}")
                    
                elif tool_name == "chat":
                    print(f"[Nuri] {intent.get('response')}")
                    
                else:
                    print(f"[SYSTEM] Unbekanntes Tool: {tool_name}")
                    print(f"[DEBUG] Raw AI: {ai_response_text}")

            except json.JSONDecodeError:
                # Falls die KI mal kein sauberes JSON liefert (passiert am Anfang mal)
                print(f"[Nuri (Raw)] {ai_response_text}")

        except KeyboardInterrupt:
            sys.exit(0)
        except Exception as e:
            print(f"[ERROR] {e}")

if __name__ == "__main__":
    main()