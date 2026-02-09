# 1. BASIS: Wir starten mit einem schlanken Linux, auf dem Python 3.12 installiert ist
FROM python:3.12-slim

# 2. OPTIMIERUNG: Verhindert, dass Python .pyc Dateien schreibt (hält den Container sauber)
# und sorgt dafür, dass Logs sofort angezeigt werden (WICHTIG für unseren Loop!)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. ARBEITSPLATZ: Wir erstellen einen Ordner "app" im Container
WORKDIR /app

# 4. VORBEREITUNG: Wir kopieren erst nur die Requirements (Caching-Trick!)
COPY requirements.txt .

# 5. INSTALLATION: Wir installieren die Abhängigkeiten
RUN pip install --no-cache-dir -r requirements.txt

# 6. KOPIEREN: Jetzt kopieren wir den Rest des Codes (run.py, skills/, etc.)
COPY . .

# 7. START: Das ist der Befehl, der ausgeführt wird, wenn der Container startet
CMD ["python", "run.py"]