import time
import sys
from skills.echo_skill import echo

# Konfiguration: Wie oft soll Nuri "denken"? (Herzschlag in Sekunden)
HEARTBEAT_RATE = 5 

def main():
    print("---------------------------------------")
    print("NURI SYSTEM START - MODE: AUTONOMOUS")
    print("---------------------------------------")
    
    # Der "Agentic Loop" - Das hier läuft endlos
    while True:
        try:
            # 1. SENSE (Wahrnehmen)
            # Simulation: Wir tun so, als gäbe es ein Event (später kommt das von Home Assistant)
            print(f"[Nuri] Scanne Umgebung... (Warte auf Input)")
            
            # Hier simulieren wir ein Event
            current_event = "System Check" 
            
            # 2. THINK (Denken) & 3. ACT (Handeln)
            # Wir nutzen deinen Echo-Skill zum Testen
            result = echo(current_event)
            print(f"[ACTION] Ausgeführter Skill: {result}")
            
            # 4. SLEEP (Warten)
            # Wichtig: Spart CPU-Ressourcen
            time.sleep(HEARTBEAT_RATE)
            
        except KeyboardInterrupt:
            # Sauberer Shutdown wenn du STRG+C drückst im Terminal
            print("\n[Nuri] Shutdown initiiert. Gute Nacht.")
            sys.exit(0)
        except Exception as e:
            # Crash-Schutz
            print(f"[ERROR] Kritischer Fehler im Loop: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()