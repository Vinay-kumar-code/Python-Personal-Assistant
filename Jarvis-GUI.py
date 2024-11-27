import win32com.client
import os
import subprocess
import webbrowser
import datetime
import ollama
from langchain_ollama import OllamaLLM
import tkinter as tk
from tkinter import scrolledtext
import threading
import whisper
import sounddevice as sd
import numpy as np
import torch
import tempfile
import wavio
import os
#FFMPEG File path for recording voice
os.environ[
    "PATH"] += os.pathsep + r"Your FFMPEG Path "

# Initialize TTS and model
speaker = win32com.client.Dispatch("SAPI.SpVoice")
model = OllamaLLM(model="jarvis")

# Load Whisper model (use "base" for faster processing or "small", "medium", "large" for more accuracy)
whisper_model = whisper.load_model("small.en")  # You can replace "base" with "small", "medium", or "large"

# Control flags
running = False
paused = False


# Function to call the model in a threaded manner
def chat(query):
    global running, paused
    stream = ollama.chat(
        model='jarvis',
        messages=[{'role': 'user', 'content': query}],
        stream=True,
    )
    result = ""
    for chunk in stream:
        if not running:  # Check if stop is called
            break
        if paused:  # Pause functionality
            while paused:
                continue
        result += chunk['message']['content']
        chat_display.insert(tk.END, chunk['message']['content'])
        chat_display.yview(tk.END)  # Auto-scroll to the bottom
    return result


def Hello():
    # This function is for when the assistant
    # is called it will say hello and then
    # take query
    speaker.Speak("hello sir I am Jarvis your assistant. How can i help you")


# Function to make Jarvis speak
def say(text):
    speaker.Speak(text)


# Offline voice recognition using Whisper
def takeCommandOffline():
    # Record audio from the microphone using sounddevice
    chat_display.insert(tk.END, "Listening for offline voice input...\n")

    fs = 16000  # Sample rate (16000 for Whisper)
    seconds = 5  # Duration of the recording

    # Record audio
    recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait()  # Wait until the recording is finished

    # Save the recording to a temporary WAV file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
        wavio.write(tmp_file.name, recording, fs, sampwidth=2)
        tmp_filename = tmp_file.name

    # Use Whisper to transcribe the audio
    result = whisper_model.transcribe(tmp_filename)
    text = result['text'].strip()

    if text:
        chat_display.insert(tk.END, f"User said: {text}\n")
        return text
    else:
        chat_display.insert(tk.END, "Could not understand the audio.\n")
        return ""


# Function to handle user query from text input or mic
def handle_query(query=None):
    global running, paused
    if query is None:
        query = user_input.get()  # Get input from text field if query is not passed
    chat_display.insert(tk.END, f"User: {query}\n")
    running = True  # Start processing
    paused = False  # Ensure it is not paused
    threading.Thread(target=process_query, args=(query,)).start()


# Main process function
def process_query(query):
    global running, paused
    if not running:
        return
    sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"],
             ["google", "https://www.google.com"], ["Google", "https://www.google.co.in"],
             ["Facebook", "https://www.facebook.com"],
             ["Instagram", "https://www.instagram.com"],
             ["Amazon", "https://www.amazon.in"],
             ["Flipkart", "https://www.flipkart.com"],
             ["Wikipedia", "https://www.wikipedia.org"],
             ["LinkedIn", "https://www.linkedin.com"],
             ["Netflix", "https://www.netflix.com"],
             ["Reddit", "https://www.reddit.com"],
             ["Quora", "https://www.quora.com"],
             ["Twitter", "https://www.twitter.com"],
             ["Hotstar", "https://www.hotstar.com"],
             ["Zomato", "https://www.zomato.com"],
             ["Paytm", "https://www.paytm.com"],
             ["Swiggy", "https://www.swiggy.com"],
             ["Book My Show", "https://www.bookmyshow.com"],
             ["Money control", "https://www.moneycontrol.com"],
             ["Myntra", "https://www.myntra.com"],
             ["Flipkart Grocery", "https://www.flipkartgrocery.com"]]
  #You can add more sites and its keyword for trigger.
    for site in sites:
        if f"Open {site[0]}".lower() in query.lower():
            say("Opening sir...")
            webbrowser.open(site[1])
            return

    def tellDay():
        # This function is for telling the
        # day of the week
        day = datetime.datetime.today().weekday() + 1

        # this line tells us about the number
        # that will help us in telling the day
        Day_dict = {1: 'Monday', 2: 'Tuesday',
                    3: 'Wednesday', 4: 'Thursday',
                    5: 'Friday', 6: 'Saturday',
                    7: 'Sunday'}

        if day in Day_dict.keys():
            day_of_the_week = Day_dict[day]
            print(day_of_the_week)
            speaker.Speak("The day is " + day_of_the_week)

    if "open music" in query.lower():
        musicPath = r"Your music files path"
        os.system(f"start {musicPath}")
        return

    elif "the time" in query.lower():
        hour = datetime.datetime.now().strftime("%H")
        minute = datetime.datetime.now().strftime("%M")
        say(f"Sir, the time is {hour}:{minute}")
        return

    elif "open brave".lower() in query.lower():
        app ="Brave"
        os.startfile(app)
    elif "open visual studio code".lower() in query.lower():
        app = "Visual Studio Code.lnk"
        os.startfile(app)
    elif "open android studio".lower() in query.lower():
        app ="Android Studio.lnk"
        os.startfile(app)
    elif "open virtual box".lower() in query.lower():
        app ="VirtualBox.lnk"
        os.startfile(app)
    elif "open calculator".lower() in query.lower():
        os.system("calc")
        speaker.Speak("Opening Calculator")
    elif "shutdown".lower() in query.lower():
        os.system("shutdown /s /t 1")
        speaker.Speak("Shutting Down")
    elif "open notepad".lower() in query.lower():
        os.system("notepad.exe")
        speaker.Speak("Opening Notepad")
    elif "the day".lower() in query.lower():
        tellDay()
    elif "hello".lower() in query.lower():
        Hello()






    elif "Jarvis Quit".lower() in query.lower():
        exit()

    elif "reset chat".lower() in query.lower():
        chat_display.delete(1.0, tk.END)
        return

    else:
        chat_response = chat(query)
        if running:  # Only say the response if not stopped
            say(chat_response)


# Function to stop (Exit) Jarvis from processing
def exit_jarvis():
    global running
    running = False  # Stop any ongoing process
    app.quit()


# Function to pause Jarvis temporarily
def pause_jarvis():
    global paused
    paused = True  # Pause the ongoing process
    chat_display.insert(tk.END, "Jarvis is paused.\n")


# Function to restart Jarvis after pause
def restart_jarvis():
    global paused
    paused = False  # Resume the paused process
    chat_display.insert(tk.END, "Jarvis is resuming...\n")


# GUI setup
app = tk.Tk()
app.title("Jarvis A.I")

# Text display for chat history
chat_display = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=50, height=20)
chat_display.grid(column=0, row=0, padx=10, pady=10)

# Input box for user
user_input = tk.Entry(app, width=50)
user_input.grid(column=0, row=1, padx=10, pady=10)

# Button to send the query
send_button = tk.Button(app, text="Send", command=lambda: handle_query())
send_button.grid(column=0, row=2, padx=10, pady=10)

# Button to capture microphone input using Whisper (offline)
mic_button = tk.Button(app, text="Use Mic (Offline)",
                       command=lambda: threading.Thread(target=lambda: handle_query(takeCommandOffline())).start())
mic_button.grid(column=0, row=3, padx=10, pady=10)

# Buttons for Stop (Exit), Pause, Restart in one row
button_frame = tk.Frame(app)
button_frame.grid(column=0, row=4, padx=10, pady=10)

# Stop button (renamed to Exit)
exit_button = tk.Button(button_frame, text="Exit", command=exit_jarvis)
exit_button.pack(side=tk.LEFT, padx=5)

# Pause button
pause_button = tk.Button(button_frame, text="Pause", command=pause_jarvis)
pause_button.pack(side=tk.LEFT, padx=5)

# Restart button
restart_button = tk.Button(button_frame, text="Restart", command=restart_jarvis)
restart_button.pack(side=tk.LEFT, padx=5)

# Start the GUI event loop
app.mainloop()
