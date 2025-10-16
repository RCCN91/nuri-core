# scripts/start-voice.ps1
# Wechselt ins Projektverzeichnis
cd C:\Users\RCCN\nuri-dev\nuri-core

# Aktiviert die virtuelle Umgebung
.\.venv\Scripts\Activate.ps1

# Startet den Voice-Loop
python gateway/voice.py
