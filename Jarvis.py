import win32com.client
import os
import subprocess
import webbrowser
import datetime
import ollama
import whisper
import sounddevice as sd
import numpy as np
import torch
import tempfile
import wavio
import requests  
from huggingface_hub import InferenceClient  
from PIL import Image
import io

# FFMPEG PATH for recording voice to whisper model
os.environ["PATH"] += os.pathsep + r"your ffmpeg path"

speaker = win32com.client.Dispatch("SAPI.SpVoice")
whisper_model = whisper.load_model("small.en")

# Hugging Face API 
HUGGINGFACE_API_KEY = "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"  # Add your API token
client = InferenceClient(api_key=HUGGINGFACE_API_KEY)
HUGGINGFACE_MODEL = "meta-llama/Llama-3.2-11B-Vision-Instruct"

# Control flags
running = False
paused = False


def Hello():
    speaker.Speak("hello sir I am Jarvis your assistant. How can i help you")

# Function to check internet connection
def is_connected():
    try:
        requests.get('https://www.google.com', timeout=3)
        return True
    except requests.ConnectionError:
        return False


# Function to create an image using Hugging Face API
def create_image(prompt):
    print("Creating an image using Hugging Face...")

    API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

    # Make the request to the API to generate an image based on the prompt
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})

    # If the request is successful, proceed to save and open the image
    if response.status_code == 200:
        image_bytes = response.content
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as img_file:
            img_file.write(image_bytes)
            img_path = img_file.name

        # Open the image using the default viewer
        print(f"Image created and saved at {img_path}. Opening the image...")
        Image.open(img_path).show()  # This opens the image in the default viewer
    else:
        print(f"Failed to create image: {response.status_code}")

def call_huggingface_model(query):
    print("Using Hugging Face for text completion...")

    response = client.chat_completion(
        model=HUGGINGFACE_MODEL,
        messages=[{"role": "user", "content": query}],
        max_tokens=500,
    )

    return response.choices[0].message['content']


# Function to call Ollama model for offline 
def call_ollama_model(query):
    global running, paused
    stream = ollama.chat(
        model='jarvis',
        messages=[{'role': 'user', 'content': query}],
        stream=True,
    )
    result = []
    for chunk in stream:
        if not running:  
            break
        if paused:  
            while paused:
                continue
        result.append(chunk['message']['content'])

    
    full_response = ''.join(result)
    return full_response


# Function to make Jarvis speak
def say(text):
    speaker.Speak(text)


# Offline voice recognition using Whisper
def takeCommandOffline():
    print("Listening for offline voice input...")

    fs = 16000  # Sample rate
    seconds = 5  # Duration of recording

    # Record audio
    recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait()  

    
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
        wavio.write(tmp_file.name, recording, fs, sampwidth=2)
        tmp_filename = tmp_file.name

    # Use Whisper to transcribe the audio
    result = whisper_model.transcribe(tmp_filename)
    text = result['text'].strip()

    if text:
        print(f"User said: {text}")
        return text
    else:
        print("Could not understand the audio.")
        return ""


# Function to handle online speech recognition (if internet is available)
def takeCommandOnline():
    import speech_recognition as sr
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening online...")
        audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio)
            print(f"User said: {query}")
            return query
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return ""
        except sr.RequestError:
            print("Could not request results; check your network connection")
            return ""


# Main process function
def process_query(query):
    global running, paused
    chat_response = ""  
    if not running:
        return
    sites = [["youtube", "https://www.youtube.com"],
    ["wikipedia", "https://www.wikipedia.com"],
    ["google", "https://www.google.com"],
    ["Facebook", "https://www.facebook.com"],
    ["Amazon", "https://www.amazon.in"],
    ["Flipkart", "https://www.flipkart.com"],
    ["Reddit", "https://www.reddit.com"],
    ["Quora", "https://www.quora.com"],
    ["Zomato", "https://www.zomato.com"],
    ["Paytm", "https://www.paytm.com"],
    ["Swiggy", "https://www.swiggy.com"],
    ["Book My Show", "https://www.bookmyshow.com"],
    ["Money control", "https://www.moneycontrol.com"],
    ["Myntra", "https://www.myntra.com"],
    ["Flipkart Grocery", "https://www.flipkartgrocery.com"]]
    for site in sites:
        if f"Open {site[0]}".lower() in query.lower():
            say("Opening sir...")
            webbrowser.open(site[1])
            return

    def tellDay():
        
    
        day = datetime.datetime.today().weekday() + 1

        
        Day_dict = {1: 'Monday', 2: 'Tuesday',
                    3: 'Wednesday', 4: 'Thursday',
                    5: 'Friday', 6: 'Saturday',
                    7: 'Sunday'}

        if day in Day_dict.keys():
            day_of_the_week = Day_dict[day]
            print(day_of_the_week)
            speaker.Speak("The day is " + day_of_the_week)

    if "open music player " in query.lower():
        musicPath = r"music file path"
        os.system(f"start {musicPath}")
        return

    elif "the time" in query.lower():
        hour = datetime.datetime.now().strftime("%H")
        minute = datetime.datetime.now().strftime("%M")
        say(f"Sir, the time is {hour}:{minute}")
        return

    elif "open brave".lower() in query.lower():
        app=r"C:\Users\vinay\OneDrive\Documents\Shortcuts\Brave"
        os.startfile(app)
    #write same code for your desired softwares/applications
    elif "shutdown".lower() in query.lower():
        os.system("shutdown /s /t 1")
        speaker.Speak("Shutting Down")

    elif "the day".lower() in query.lower():
        tellDay()
    elif "hello".lower() in query.lower():
        Hello()
    elif "hi".lower() in query.lower():
        Hello()
    elif "hey jarvis".lower() in query.lower():
        Hello()
    elif "how are you".lower() in query.lower():
        Hello()


    elif "create an image" in query.lower():
        prompt = input("Enter the prompt for image generation: ")
        if is_connected():
            create_image(prompt)
            chat_response = f"Image created and saved successfully."
        else:
            chat_response = "No internet connection. Unable to create image."
            print(chat_response)
            say(chat_response)

    # For text-based queries
    else:
        # If internet is available, use Hugging Face model, else use Ollama (offline)
        if is_connected():
            chat_response = call_huggingface_model(query)
        else:
            chat_response = call_ollama_model(query)

    if running:
        print(chat_response)
        say(chat_response)



# Function to stop 
def stop_jarvis():
    global running
    running = False


# Main loop to handle input
def main():
    global running, paused
    running = True
    while running:

        user_input = input("You: ").lower()

        if "use mic" in user_input:
            
            if is_connected():
                query = takeCommandOnline()  # online
            else:
                query = takeCommandOffline()  #offline
        else:
            query = user_input

        process_query(query)


if __name__ == "__main__":
    speaker.Speak("hello sir I am Jarvis your assistant. How can i help you")
    root.after(0, main)  
    root.mainloop()  
