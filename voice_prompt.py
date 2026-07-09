import speech_recognition as sr
from vosk import Model, KaldiRecognizer
import os
import json
import wave
import tkinter as tk
from tkinter import messagebox

VOSK_MODEL_PATH = "models/vosk-model-small-en-us-0.15"

def get_voice_prompt():
    if not os.path.exists(VOSK_MODEL_PATH):
        messagebox.showerror("Error", "Vosk model not found!")
        return None

    model = Model(VOSK_MODEL_PATH)
    recognizer = sr.Recognizer()

    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Voice Prompt", "Please speak your instruction after pressing OK.")

    with sr.Microphone() as source:
        print("🎤 Listening...")
        audio = recognizer.listen(source, phrase_time_limit=10)

    print("🔄 Transcribing...")

    try:
        with open("temp.wav", "wb") as f:
            f.write(audio.get_wav_data())

        wf = wave.open("temp.wav", "rb")
        rec = KaldiRecognizer(model, wf.getframerate())
        rec.SetWords(True)

        results = []
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                results.append(result.get("text", ""))
        final_result = json.loads(rec.FinalResult()).get("text", "")
        results.append(final_result)

        full_text = " ".join(results).strip()
        return full_text if full_text else None

    except Exception as e:
        print("❌ Voice Error:", e)
        return None
