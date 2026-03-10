import datetime
import os
import sys
import time
import webbrowser
import pyautogui
import pyttsx3
import speech_recognition as sr
import json
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import random
import psutil
import requests

# Load training components
with open("intents.json") as file:
    data = json.load(file)

model = load_model("chat_model.h5")
with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)
with open("label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)

# Text-to-speech engine setup
def initialize_engine():
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)
    return engine


def speak(text):
    engine = initialize_engine()
    engine.say(text)
    engine.runAndWait()

# Speech recognition
def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
    except Exception:
        speak("Pardon me, please say that again.")
        return "None"
    return query

# Greet user
def cal_day():
    day = datetime.datetime.today().weekday() + 1
    day_dict = {
        1: "Monday", 2: "Tuesday", 3: "Wednesday",
        4: "Thursday", 5: "Friday", 6: "Saturday", 7: "Sunday"
    }
    return day_dict.get(day, "")

def wishMe():
    hour = int(datetime.datetime.now().hour)
    t = time.strftime("%I:%M %p")
    day = cal_day()
    if hour < 12:
        speak(f"Good morning, it's {day} and the time is {t}")
    elif hour < 16:
        speak(f"Good afternoon, it's {day} and the time is {t}")
    else:
        speak(f"Good evening, it's {day} and the time is {t}")

# Social media commands
def social_media(command):
    links = {
        'facebook': "https://www.facebook.com/",
        'whatsapp': "https://web.whatsapp.com/",
        'discord': "https://discord.com/",
        'instagram': "https://www.instagram.com/"
    }
    for key in links:
        if key in command:
            speak(f"Opening your {key}")
            webbrowser.open(links[key])
            return
    speak("No matching platform found.")

# Open/close apps
def openApp(command):
    apps = {
        "calculator": 'C:\\Windows\\System32\\calc.exe',
        "notepad": 'C:\\Windows\\System32\\notepad.exe',
        "paint": 'C:\\Windows\\System32\\mspaint.exe'
    }
    for key, path in apps.items():
        if key in command:
            speak(f"Opening {key}")
            os.startfile(path)

def closeApp(command):
    apps = {
        "calculator": "calc.exe",
        "notepad": "notepad.exe",
        "paint": "mspaint.exe"
    }
    for key, proc in apps.items():
        if key in command:
            speak(f"Closing {key}")
            os.system(f"taskkill /f /im {proc}")

# System status
def condition():
    usage = str(psutil.cpu_percent())
    speak(f"CPU is at {usage} percent")
    battery = psutil.sensors_battery()
    percentage = battery.percent
    speak(f"Battery is at {percentage} percent")
    if percentage >= 80:
        speak("Battery is sufficient.")
    elif 40 <= percentage < 80:
        speak("Consider plugging in the charger.")
    else:
        speak("Battery is low. Please charge soon.")

# Schedule
def schedule():
    day = cal_day().lower()
    week = {
        "monday": "From 9:00 to 9:50 Algorithms, 10:00 to 11:50 System Design, afternoon Programming Lab.",
        "tuesday": "9:00 Web Dev, 11:00 Database, afternoon Open Source Lab.",
        "wednesday": "Morning ML, OS, and Ethics; afternoon Software Workshop.",
        "thursday": "CN, Cloud Computing, and Cybersecurity Lab.",
        "friday": "AI, Advanced Programming, UI/UX, Capstone in afternoon.",
        "saturday": "Capstone meetings and I&E class.",
        "sunday": "Relax! But review your project deadlines."
    }
    speak("Boss, your schedule for today is:")
    speak(week.get(day, "No schedule found."))

# Google browsing
def browsing(query):
    if 'google' in query:
        speak("What should I search on Google?")
        s = command().lower()
        webbrowser.open(f"https://www.google.com/search?q={s}")

# Weather
def get_weather():
    api_key = "8ef61edcf1c576d65d836254e11ea420"
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    speak("What city should I check the weather for?")
    city_name = command()
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    data = response.json()
    if data["cod"] != "404":
        y = data["main"]
        temp = y["temp"]
        humidity = y["humidity"]
        weather = data["weather"][0]["description"]
        report = f"Temperature: {temp} Kelvin, Humidity: {humidity}%, Weather: {weather}"
        speak(report)
    else:
        speak("City not found")

# Play music
def play_music():
    music_dir = "C:\\Users\\hp\\Desktop\\jarvisai\\music"  # CHANGE THIS PATH
    try:
        songs = os.listdir(music_dir)
        songs = [song for song in songs if song.endswith(".mp3")]

        if len(songs) == 0:
            speak("No music files found.")
            return

        song = random.choice(songs)
        speak("Playing music for you.")
        os.startfile(os.path.join(music_dir, song))

    except Exception as e:
        speak("Sorry, I couldn't play the music.")
        print(e)


# Main loop
if __name__ == "__main__":
    wishMe()
    speak("Loading your personal AI assistant, Jarvis...")
    while True:
        query = command().lower()
        if any(x in query for x in ['facebook', 'discord', 'whatsapp', 'instagram']):
            social_media(query)
        elif "schedule" in query or "timetable" in query:
            schedule()
        elif "volume up" in query:
            pyautogui.press("volumeup")
            speak("Volume increased")
        elif "volume down" in query:
            pyautogui.press("volumedown")
            speak("Volume decreased")
        elif "mute" in query:
            pyautogui.press("volumemute")
            speak("Volume muted")
        elif "open" in query:
            openApp(query)
        elif "close" in query:
            closeApp(query)
        elif "weather" in query:
            get_weather()
        elif "system condition" in query:
            speak("Checking system status")
            condition()
        elif "open google" in query:
            browsing(query)
        elif any(q in query for q in ["what", "who", "how", "hi", "hello", "thanks"]):
            seq = pad_sequences(tokenizer.texts_to_sequences([query]), maxlen=20, truncating='post')
            result = model.predict(seq)
            tag = label_encoder.inverse_transform([np.argmax(result)])
            for intent in data["intents"]:
                if intent["tag"] == tag:
                    speak(random.choice(intent["responses"]))
        elif "time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")
        elif "play music" in query or "play song" in query or "music" in query:
            play_music()
        elif "stop music" in query:
            speak("Stopping the music.")
            os.system("taskkill /f /im wmplayer.exe")

        elif any(x in query for x in ["who made you", "who created you"]):
            speak("I was created by AI Robosoft.")
        elif "exit" in query or "bye" in query or "stop" in query:
            speak("Jarvis shutting down. Goodbye!")
            print("Jarvis shut down.")
            break
