import random
import speech_recognition as sr
import tkinter as tk
from tkinter import filedialog, messagebox

recognizer = sr.Recognizer()

def guess_from_text(command):
    try:
        guess = int(command.strip())
        number_to_guess = random.randint(1, 100)
        result = f"You said: {guess}\n"

        if guess == number_to_guess:
            result += f"🎉 Correct! You guessed it right: {number_to_guess}"
        else:
            result += f"❌ Wrong! The correct number was: {number_to_guess}"

        result_label.config(text=result)
    except ValueError:
        result_label.config(text="❗ Please speak a valid number.")

def listen_from_file():
    file_path = filedialog.askopenfilename(filetypes=[("WAV Files", "*.wav")])
    if not file_path:
        return

    try:
        with sr.AudioFile(file_path) as source:
            status_label.config(text="🎧 Processing file...")
            audio_data = recognizer.record(source)
            status_label.config(text="🧠 Recognizing from file...")
            command = recognizer.recognize_google(audio_data)
            guess_from_text(command)

    except sr.UnknownValueError:
        result_label.config(text="❌ Could not understand the audio.")
    except sr.RequestError:
        result_label.config(text="⚠️ Speech recognition service failed.")
    except Exception as e:
        result_label.config(text=f"Error: {e}")

def listen_from_mic():
    try:
        with sr.Microphone() as source:
            status_label.config(text="🎤 Listening... Speak a number (1–100)")
            app.update()
            audio_data = recognizer.listen(source, timeout=5)
            status_label.config(text="🧠 Recognizing from mic...")
            command = recognizer.recognize_google(audio_data)
            guess_from_text(command)

    except sr.UnknownValueError:
        result_label.config(text="❌ Could not understand your voice.")
    except sr.RequestError:
        result_label.config(text="⚠️ Speech recognition service failed.")
    except Exception as e:
        result_label.config(text=f"Error: {e}")

# GUI Setup
app = tk.Tk()
app.title("🎲 Guess the Number - Voice Game")
app.geometry("480x400")
app.config(bg="#f0f8ff")

tk.Label(app, text="🎙️ Voice Guessing Game", font=("Helvetica", 17, "bold"), bg="#f0f8ff").pack(pady=20)

tk.Button(app, text="🎤 Speak Guess (Mic)", command=listen_from_mic,
          font=("Arial", 13), bg="#2196f3", fg="white", padx=10, pady=6).pack(pady=10)

tk.Button(app, text="📂 Choose WAV File", command=listen_from_file,
          font=("Arial", 13), bg="#4caf50", fg="white", padx=10, pady=6).pack(pady=10)

status_label = tk.Label(app, text="Ready.", font=("Arial", 12), fg="blue", bg="#f0f8ff")
status_label.pack(pady=10)

result_label = tk.Label(app, text="", font=("Arial", 12), bg="#f0f8ff", wraplength=400)
result_label.pack(pady=20)

tk.Label(app, text="🎯 Try saying a number between 1 and 100.", font=("Arial", 11), bg="#f0f8ff", fg="#666").pack(pady=5)

app.mainloop()
