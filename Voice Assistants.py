import speech_recognition as sr
import pyttsx3
import os
import tkinter as tk
from tkinter import filedialog, messagebox

# Initialize TTS
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Speech recognizer
recognizer = sr.Recognizer()

def execute_command(command):
    if "notepad" in command:
        speak("Opening Notepad")
        os.system("notepad")
    elif "calculator" in command or "calc" in command:
        speak("Opening Calculator")
        os.system("calc")
    elif "paint" in command:
        speak("Opening Paint")
        os.system("mspaint")
    elif "command prompt" in command or "cmd" in command:
        speak("Opening Command Prompt")
        os.system("start cmd")
    elif "chrome" in command:
        speak("Opening Google Chrome")
        os.system("start chrome")
    elif "explorer" in command or "file manager" in command:
        speak("Opening File Explorer")
        os.system("explorer")
    else:
        speak("Sorry, I don't know how to open that.")
        messagebox.showinfo("Command Not Recognized", "Sorry, I don't know how to open that.")

def listen_from_file(file_path):
    try:
        with sr.AudioFile(file_path) as source:
            status_label.config(text="🔊 Listening to the audio file...")
            app.update()
            audio = recognizer.record(source)
            command = recognizer.recognize_google(audio)
            spoken_text.set(f"🎤 You said (file): {command}")
            return command.lower()
    except Exception as e:
        messagebox.showerror("Error", f"❌ Could not process audio:\n{e}")
        return ""

def choose_file_and_execute():
    file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
    if file_path:
        command = listen_from_file(file_path)
        if command:
            execute_command(command)
        status_label.config(text="Ready.")

def listen_from_mic():
    try:
        with sr.Microphone() as source:
            status_label.config(text="🎙️ Listening from mic... Speak now")
            app.update()
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5)
        command = recognizer.recognize_google(audio)
        spoken_text.set(f"🎤 You said (mic): {command}")
        execute_command(command.lower())
    except sr.UnknownValueError:
        messagebox.showwarning("Could Not Understand", "❌ Could not understand your voice.")
    except sr.RequestError:
        messagebox.showerror("API Error", "❌ Could not reach Google Speech API.")
    except Exception as e:
        messagebox.showerror("Error", f"❌ Mic error: {e}")
    finally:
        status_label.config(text="Ready.")

# GUI setup
app = tk.Tk()
app.title("Voice Command Launcher")
app.geometry("550x420")
app.configure(bg="#e3f2fd")

tk.Label(app, text="Voice-Controlled App Launcher", font=("Helvetica", 18, "bold"), bg="#e3f2fd", fg="#1565c0").pack(pady=20)

tk.Button(app, text="🎤 Speak Now (Mic Input)", command=listen_from_mic,
          font=("Arial", 14), bg="#43a047", fg="white", padx=10, pady=6).pack(pady=10)

tk.Button(app, text="📂 Choose WAV File & Execute", command=choose_file_and_execute,
          font=("Arial", 14), bg="#1976d2", fg="white", padx=10, pady=6).pack(pady=10)

status_label = tk.Label(app, text="Ready.", font=("Arial", 12), bg="#e3f2fd", fg="#333")
status_label.pack()

spoken_text = tk.StringVar()
spoken_label = tk.Label(app, textvariable=spoken_text, font=("Arial", 12), bg="#e3f2fd", wraplength=500)
spoken_label.pack(pady=10)

tk.Label(app, text="Say commands like:\n'open notepad', 'open calculator', 'open chrome', etc.",
         font=("Arial", 11), bg="#e3f2fd", fg="#555").pack(pady=10)

app.mainloop()
