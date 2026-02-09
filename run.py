import time
import sys
import requests
import json

# Konfiguration
HEARTBEAT_RATE = 5
# Wir nutzen localhost, weil Ollama lokal auf deinem PC läuft
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"  # Falls du tinyllama hast, ändere das hier zu "tinyllama"

def think(prompt):
    """Sendet einen Gedanken an das lokale Gehirn (Ollama)"""
    try:
        payload = {
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
        response = requests.post(OLLAMA_URL, json=payload)
        return response.json()['response']
    except Exception as e:
        return f"Gehirn-Fehler: {e}"

def main():
    print("---------------------------------------")
    print(f"NURI SYSTEM START - BRAIN: {MODEL}")
    print("---------------------------------------")
    
    while True:
        try:
            print(f"\n[Nuri] Scanne Umgebung...")
            
            # 1. SENSE: Wir simulieren eine Eingabe
            user_input = "Hallo Nuri! Wie ist dein Status?"
            print(f"[INPUT] {user_input}")

            # 2. THINK: Wir fragen die KI
            print("[Nuri] Denke nach...")
            answer = think(f"Du bist Nuri, ein intelligenter Hausassistent. Antworte kurz und prägnant auf Deutsch. User: {user_input}")
            
            # 3. ACT: Antwort ausgeben
            print(f"[OUTPUT] {answer}")
            
            # 4. SLEEP
            time.sleep(HEARTBEAT_RATE)
            
        except KeyboardInterrupt:
            print("\n[Nuri] Shutdown.")
            sys.exit(0)

if __name__ == "__main__":
    main()