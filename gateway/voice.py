# gateway/voice.py
import requests
import subprocess
from faster_whisper import WhisperModel
from openwakeword import HotwordDetector
from piper_tts import TTS

WAKE_WORD = "Nuri"
API_URL = "http://localhost:8000/echo"

# Whisper-Modell einmalig laden
whisper_model = WhisperModel("base", device="cpu")
# Piper-TTS initialisieren (nutzt standardmäßig en_GB)
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")

def listen_and_transcribe():
    segments, _ = whisper_model.transcribe("input.wav")
    return "".join(seg.text for seg in segments).strip()

def speak(text: str):
    wav = tts.tts(text)
    # piped zu deinem Lautsprecher-Player
    subprocess.run(["powershell", "-c", f"[System.Console]::Beep(); Start-Process -FilePath powershell -ArgumentList \"-c (New-Object Media.SoundPlayer '{wav}').PlaySync()\""])

def main_loop():
    detector = HotwordDetector(WAKE_WORD)
    print("Hotword detector ready – sag ‘Hey Nuri’")
    for _ in detector:
        print("Wake-Word erkannt, bitte sprechen…")
        # hier müsstest du deine Audioaufnahme starten und nach 4 Sekunden als input.wav speichern
        user_text = listen_and_transcribe()
        print("Du sagtest:", user_text)
        # Anfrage an dein Echo-Endpoint
        resp = requests.post(API_URL, json={"text": user_text})
        reply = resp.json().get("reply", "")
        print("Nuri antwortet:", reply)
        speak(reply)

if __name__ == "__main__":
    main_loop()
