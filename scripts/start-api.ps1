# scripts/start-api.ps1
# Wechselt ins Projektverzeichnis
cd C:\Users\RCCN\nuri-dev\nuri-core

# Aktiviert die virtuelle Umgebung
.\.venv\Scripts\Activate.ps1

# Startet den FastAPI-Server
python -m uvicorn gateway.app:app --reload --host 0.0.0.0 --port 8000
