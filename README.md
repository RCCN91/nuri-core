# 🎙️ NURI Core – Personal AI Assistant

> *"Guten Abend, Sir. Wie kann ich heute behilflich sein?"*

Nuri ist ein hochmodernes, Multi-Agenten-basiertes Smart-Home-System, das auf **Llama 3** (via Ollama) läuft. Es wurde entwickelt, um eine nahtlose, Jarvis-ähnliche Interaktion zu ermöglichen – lokal, privat, ohne Cloud.

---

## 🧠 Kern-Features

- **Multi-Agenten-Architektur** – Ein intelligenter Router delegiert Aufgaben an spezialisierte Agenten (Atlas, Pythagoras, Edison). Jeder Agent hat seine eigene Persönlichkeit und Werkzeuge.
- **Proaktives Bewusstsein** – Hintergrund-Observer prüfen minütlich Zeit-Erinnerungen und lauschen via Home Assistant WebSocket auf Geräte-Events.
- **Langzeitgedächtnis** – SQLite-basiertes Gedächtnis speichert Gespräche, Notizen und Erinnerungen persistent über Sessions hinweg.
- **Voice-First** – Vollständig lokale Sprachverarbeitung mit `openwakeword` (Wake Word) und `faster-whisper` (Transkription). Keine Cloud-Abhängigkeit.
- **Smart Home Integration** – Direkte Steuerung von Home Assistant Geräten über REST API und Echtzeit-Event-Streaming via WebSocket.
- **Notiz-System** – Sprachbasierter Diktiermodus: Nuri hört zu, bis du „Notiz Ende" sagst, und speichert alles automatisch.

---

## 👥 Identitäten

| Rolle | Name |
|---|---|
| Admin & Lead Developer | Nick |
| Autorisierte Nutzerin | Shayenne |

---

## 👨‍💼 Agenten-Übersicht

### 🗺️ Nuri Router
Der zentrale Verteiler. Analysiert jede Anfrage und entscheidet, welcher Spezialist antwortet. Antwortet nie selbst – er leitet nur weiter.

### 🏠 Atlas – Smart Home & Erinnerungen
Kumpelhaft, direkt, fürsorglich und vorausschauend. Atlas steuert Geräte, verwaltet Notizen und setzt Erinnerungen. Er vergisst nichts.
- **Tools:** `ha_control`, `save_note`, `list_notes`, `add_reminder`

### 🦉 Pythagoras – Weiser Gesprächspartner
Stoiker. Ruhig, nicht wertend. Hilft beim Denken, gibt keine vorschnellen Ratschläge. Redet wenig, aber mit Gewicht.
- **Tools:** nur `chat`

### ⚡ Edison – Tech-Nerd & Wissenslieferant
Chaotisch enthusiastisch. Liebt Fakten, Wissenschaft und Technik. Kann die Gesprächshistorie durchsuchen.
- **Tools:** `search_history`, `chat`

---

## 🗂️ Projektstruktur

```
nuri-core/
├── gateway/
│   ├── app.py          # FastAPI REST-Gateway (/health, /echo, /chat)
│   └── voice.py        # Voice-Client: Wake Word, Transkription, proaktive Threads
├── nuri_sdk/
│   ├── kernel.py       # Multi-Agenten-Orchestrierung (Router → Spezialist)
│   ├── memory.py       # SQLite: Gespräche, Notizen, Erinnerungen
│   ├── personas.py     # System-Prompts für alle Agenten
│   └── logger.py       # Zentrales Logging
├── skills/
│   └── registry.py     # Tool-Registry: ha_control, save_note, add_reminder, ...
├── run.py              # CLI-Einstiegspunkt (Text-Interface)
├── requirements.txt
└── .env                # Geheime Konfiguration (nicht auf GitHub!)
```

---

## 🛠️ Installation & Setup

### 1. Repository klonen

```bash
git clone <repo-url>
cd nuri-core
```

### 2. Virtuelle Umgebung erstellen & Abhängigkeiten installieren

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
# oder: venv\Scripts\activate  (Windows)

pip install -r requirements.txt
```

> **Hinweis zu openwakeword auf Python 3.12 (Linux):**
> `tflite-runtime` ist nicht kompatibel. Daher mit `--no-deps` installieren:
> ```bash
> pip install openwakeword --no-deps
> pip install onnxruntime tqdm scipy scikit-learn
> ```

### 3. Ollama & Llama 3 installieren

```bash
# Ollama installieren (https://ollama.com)
ollama pull llama3
```

### 4. `.env` Datei anlegen

```
# Home Assistant
HA_URL=http://192.168.178.50:8123
HA_TOKEN=dein_langzeit_token_hier

# Nutzeridentitäten
USER_NAME=Shayenne
```

> ⚠️ **Diese Datei darf NIEMALS auf GitHub landen!** Sie ist in `.gitignore` eingetragen.

---

## 🚀 Starten

### Text-Interface (CLI)

```bash
python run.py
```

### REST-API Gateway

```bash
uvicorn gateway.app:app --reload
```

API ist erreichbar unter `http://localhost:8000`
- `GET  /health` – Systemstatus
- `POST /chat`   – `{"text": "Mach das Licht an"}` → `{"reply": "..."}`

### Voice-Client

```bash
python gateway/voice.py
```

Sag **„Hey Jarvis"** – Nuri hört zu.

---

## 🧩 Architektur-Überblick

```
Spracheingabe / Text
        ↓
  gateway/app.py  ←→  gateway/voice.py
        ↓
  NuriKernel.ask()
    ├── Schritt 1: nuri_router → entscheidet Spezialist
    └── Schritt 2: atlas / pythagoras / edison → führt Tool aus
                    ↓
              skills/registry.py
                    ↓
         Home Assistant / SQLite / Chat

  [Hintergrund]
  ├── time_reminder_worker  – prüft jede Minute Zeitbasierte Reminder
  └── ha_event_worker       – WebSocket → reagiert auf HA state_changed Events
```

---

## 🗣️ Voice-Features

| Trigger | Verhalten |
|---|---|
| *„Hey Jarvis"* | Wake Word – Nuri wird aktiv |
| *„Notiz / Merk dir..."* | Notiz-Diktiermodus startet |
| *„Notiz Ende"* | Diktiermodus endet, Notiz wird gespeichert |
| Proaktive Erinnerung | *„Kurze Unterbrechung, Shayenne... Arzttermin!"* |

---

## 🔔 Erinnerungssystem

**Zeitbasiert** (einmalig):
> *„Erinnere mich um 15 Uhr an den Arzttermin"*
> → Atlas setzt Reminder für `2026-02-17 15:00:00`
> → Um 15:00 Uhr spricht Nuri proaktiv die Erinnerung aus

**Ereignisbasiert** (wiederkehrend):
> *„Sag mir jedes 3. Mal wenn die Kaffeemaschine angeht"*
> → Atlas setzt Reminder mit `condition=switch.kaffeemaschine, interval=3`
> → Nach dem 3. `state_changed`-Event löst Nuri die Erinnerung aus

---

## 🗃️ Datenbank

SQLite unter `nuri_history.db` (nicht auf GitHub):

| Tabelle | Inhalt |
|---|---|
| `interactions` | Alle Gespräche mit Timestamp, Agent, User- und Nuri-Text |
| `notes` | Gespeicherte Notizen mit Timestamp |
| `reminders` | Erinnerungen mit Typ, Zielzeit/Entity, Intervall, Zähler |

---

## 📦 Abhängigkeiten

| Paket | Zweck |
|---|---|
| `ollama` | Llama 3 LLM (lokal) |
| `fastapi` + `uvicorn` | REST-API Gateway |
| `openwakeword` | Wake Word Erkennung |
| `faster-whisper` | Sprache → Text (lokal) |
| `sounddevice` + `scipy` | Audio-Aufnahme & Resampling |
| `websocket-client` | HA WebSocket für Event-Streaming |
| `python-dotenv` | `.env` Konfiguration |
| `sqlite3` | Langzeitgedächtnis (stdlib) |

---

## 🔒 Sicherheit

Folgende Dateien sind via `.gitignore` vom Repository ausgeschlossen:

```
.env              # HA-Token, Nutzernamen
nuri_history.db   # Gesprächshistorie, Notizen, Erinnerungen
venv/             # Virtuelle Umgebung
__pycache__/      # Python-Cache
```

---

*Built with ❤️ and Llama 3 – running 100% local.*
