import speech_recognition as sr
import os
import tkinter as tk
from tkinter import messagebox

recognizer = sr.Recognizer()

def recognize_speech():
    status_label.config(text="Listening...", fg="#1565c0")
    app.update()

    try:
        with sr.Microphone() as source:
            audio = recognizer.listen(source, timeout=5)
        try:
            text = recognizer.recognize_google(audio)
            result_label.config(text=f"From Mic: {text}", fg="#2e7d32")
        except sr.UnknownValueError:
            result_label.config(text="Could not understand the mic input.", fg="red")
        except sr.RequestError:
            result_label.config(text="Google API error from mic input.", fg="red")

    except OSError:
        status_label.config(text="Microphone not found. Trying fallback file...", fg="#ef6c00")
        fallback_file = "voice.wav"

        if not os.path.exists(fallback_file):
            result_label.config(text="Fallback file not found.", fg="red")
        else:
            with sr.AudioFile(fallback_file) as source:
                audio = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio)
                result_label.config(text=f"From File: {text}", fg="#2e7d32")
            except sr.UnknownValueError:
                result_label.config(text="Could not understand the audio in file.", fg="red")
            except sr.RequestError:
                result_label.config(text="Google API error from file input.", fg="red")
    
    status_label.config(text="Ready.", fg="black")

# GUI Setup
app = tk.Tk()
app.title("Speech Recognizer")
app.geometry("500x300")
app.configure(bg="#e3f2fd")

tk.Label(app, text="Speech Recognition App", font=("Helvetica", 18, "bold"), bg="#e3f2fd", fg="#0d47a1").pack(pady=20)

tk.Button(app, text="Start Listening", command=recognize_speech,
          font=("Arial", 14), bg="#1976d2", fg="white", padx=10, pady=6).pack(pady=10)

status_label = tk.Label(app, text="Ready.", font=("Arial", 12), bg="#e3f2fd")
status_label.pack()

result_label = tk.Label(app, text="", font=("Arial", 12), bg="#e3f2fd", wraplength=450, justify="center")
result_label.pack(pady=15)

tk.Label(app, text="Fallback to 'voice.wav' if mic unavailable.", font=("Arial", 10), bg="#e3f2fd", fg="#555").pack(side="bottom", pady=10)

app.mainloop()
