
import datetime
import os
import sys
import time
import webbrowser
import pyautogui
import pyttsx3 #!pip install pyttsx3
import speech_recognition as sr
import json
import pygame
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import random
import numpy as np
import psutil 
import subprocess
import wolframalpha
import requests
import wikipedia
# from elevenlabs import generate, play
# from elevenlabs import set_api_key
# from api_key import api_key_data
# set_api_key(api_key_data)

# def engine_talk(query):
#     audio = generate(
#         text=query, 
#         voice='Grace',
#         model="eleven_monolingual_v1"
#     )
#     play(audio)

with open("intents.json") as file:
    data = json.load(file)

model = load_model("chat_model.h5")

with open("tokenizer.pkl", "rb") as f:
    tokenizer=pickle.load(f)

with open("label_encoder.pkl", "rb") as encoder_file:
    label_encoder=pickle.load(encoder_file)

def initialize_engine():
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-50)
    volume = engine.getProperty('volume')
    engine.setProperty('volume', volume+0.25)
    return engine

def speak(text):
    engine = initialize_engine()
    engine.say(text)
    engine.runAndWait()
'''
def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening.......", end="", flush=True)
        r.pause_threshold=1.0
        r.phrase_threshold=0.3
        r.sample_rate = 48000
        r.dynamic_energy_threshold=True
        r.operation_timeout=5
        r.non_speaking_duration=0.5
        r.dynamic_energy_adjustment=2
        r.energy_threshold=4000
        r.phrase_time_limit = 10
        # print(sr.Microphone.list_microphone_names())
        audio = r.listen(source)
    try:
        print("\r" ,end="", flush=True)
        print("Recognizing......", end="", flush=True)
        query = r.recognize_google(audio, language='en-in')
        print("\r" ,end="", flush=True)
        print(f"User said : {query}\n")
    except Exception as e:
        print("Say that again please")
        return "None"
    return query
'''
def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        speak("Pardon me, please say that again.")
        return "None"
    return query
def cal_day():
    day = datetime.datetime.today().weekday() + 1
    day_dict={
        1:"Monday",
        2:"Tuesday",
        3:"Wednesday",
        4:"Thursday",
        5:"Friday",
        6:"Saturday",
        7:"Sunday"
    }
    if day in day_dict.keys():
        day_of_week = day_dict[day]
        print(day_of_week)
    return day_of_week

def wishMe():
    hour = int(datetime.datetime.now().hour)
    t = time.strftime("%I:%M:%p")
    day = cal_day()

    if(hour>=0) and (hour<=12) and ('AM' in t):
        speak(f"Good morning , it's {day} and the time is {t}")
    elif(hour>=12)  and (hour<=16) and ('PM' in t):
        speak(f"Good afternoon , it's {day} and the time is {t}")
    else:
        speak(f"Good evening , it's {day} and the time is {t}")

def social_media(command):
    if 'facebook' in command:
        speak("opening your facebook")
        webbrowser.open("https://www.facebook.com/")
    elif 'whatsapp' in command:
        speak("opening your whatsapp")
        webbrowser.open("https://web.whatsapp.com/")
    elif 'discord' in command:
        speak("opening your discord server")
        webbrowser.open("https://discord.com/")
    elif 'instagram' in command:
        speak("opening your instagram")
        webbrowser.open("https://www.instagram.com/")
    else:
        speak("No result found")

def schedule():
    day = cal_day().lower()
    speak("Boss today's schedule is ")
    week={
    "monday": "Boss, from 9:00 to 9:50 you have Algorithms class, from 10:00 to 11:50 you have System Design class, from 12:00 to 2:00 you have a break, and today you have Programming Lab from 2:00 onwards.",
    "tuesday": "Boss, from 9:00 to 9:50 you have Web Development class, from 10:00 to 10:50 you have a break, from 11:00 to 12:50 you have Database Systems class, from 1:00 to 2:00 you have a break, and today you have Open Source Projects lab from 2:00 onwards.",
    "wednesday": "Boss, today you have a full day of classes. From 9:00 to 10:50 you have Machine Learning class, from 11:00 to 11:50 you have Operating Systems class, from 12:00 to 12:50 you have Ethics in Technology class, from 1:00 to 2:00 you have a break, and today you have Software Engineering workshop from 2:00 onwards.",
    "thursday": "Boss, today you have a full day of classes. From 9:00 to 10:50 you have Computer Networks class, from 11:00 to 12:50 you have Cloud Computing class, from 1:00 to 2:00 you have a break, and today you have Cybersecurity lab from 2:00 onwards.",
    "friday": "Boss, today you have a full day of classes. From 9:00 to 9:50 you have Artificial Intelligence class, from 10:00 to 10:50 you have Advanced Programming class, from 11:00 to 12:50 you have UI/UX Design class, from 1:00 to 2:00 you have a break, and today you have Capstone Project work from 2:00 onwards.",
    "saturday": "Boss, today you have a more relaxed day. From 9:00 to 11:50 you have team meetings for your Capstone Project, from 12:00 to 12:50 you have Innovation and Entrepreneurship class, from 1:00 to 2:00 you have a break, and today you have extra time to work on personal development and coding practice from 2:00 onwards.",
    "sunday": "Boss, today is a holiday, but keep an eye on upcoming deadlines and use this time to catch up on any reading or project work."
    }
    if day in week.keys():
        speak(week[day])

def openApp(command):
    if "calculator" in command:
        speak("opening calculator")
        os.startfile('C:\\Windows\\System32\\calc.exe')
    elif "notepad" in command:
        speak("opening notepad")
        os.startfile('C:\\Windows\\System32\\notepad.exe')
    elif "paint" in command:
        speak("opening paint")
        os.startfile('C:\\Windows\\System32\\mspaint.exe')
    time.sleep(2)  # wait for 2 seconds

def closeApp(command):
    time.sleep(2)  # Give time for the process to initialize if just opened
    if "calculator" in command:
        speak("closing calculator")
        os.system("taskkill /f /im calc.exe")
    elif "notepad" in command:
        speak("closing notepad")
        os.system("taskkill /f /im notepad.exe")
    elif "paint" in command:
        speak("closing paint")
        os.system("taskkill /f /im mspaint.exe")

#   def browsing(query):
    #if 'google' in query:
        #speak("Boss, what should i search on google..")
        #s = command().lower()
        #webbrowser.open(f"{s}")
    # elif 'edge' in query:
    #     speak("opening your microsoft edge")
    #     os.startfile()

def condition():
    usage = str(psutil.cpu_percent())
    speak(f"CPU is at {usage} percentage")
    battery = psutil.sensors_battery()
    percentage = battery.percent
    speak(f"Boss our system have {percentage} percentage battery")

    if percentage>=80:
        speak("Boss we could have enough charging to continue our recording")
    elif percentage>=40 and percentage<=75:
        speak("Boss we should connect our system to charging point to charge our battery")
    else:
        speak("Boss we have very low power, please connect to charging otherwise recording should be off...")
pygame.mixer.init()
def play_music():
    try:
        # List of music files (add your own music files here)
        music_files = ["C:\\Users\\hp\\Desktop\\jarvisai\\music\\WhatsApp Audio 2025-05-02 at 8.45.19 PM.mpeg", "C:\\Users\\hp\\Desktop\\jarvisai\\music\\WhatsApp Audio 2025-05-02 at 8.45.29 PM.mpeg", "C:\\Users\\hp\\Desktop\\jarvisai\\music\\WhatsApp Audio 2025-05-02 at 8.45.32 PM.mpeg"]

        # Choose a random song from the list
        song = random.choice(music_files)
        print(f"Playing: {song}")
        pygame.mixer.init()  # Initialize the mixer
        pygame.mixer.music.load(song)  # Replace with your music file path
        pygame.mixer.music.play()
        pygame.mixer.init()  # Initialize the mixer

        # Keep the program running until the music finishes
        while pygame.mixer.music.get_busy():
            time.sleep(1)

    except Exception as e:
        print(f"Error playing music: {e}")


if __name__ == "__main__":
    wishMe()
    speak("Loading your personal AI assistant Jarvis...")
    speak("how can i help you?")
    # engine_talk("Allow me to introduce myself I am Jarvis, the virtual artificial intelligence and I'm here to assist you with a variety of tasks as best I can, 24 hours a day seven days a week.")
    while True:
        query = command().lower()
        #query  = input("Enter your command-> ")
        if "how are you" in query or "how about you" in query or "are you ok" in query  or "how r u" in query or "how's it going" in query or "how are you doing" in query:
            speak("I'm doing great, thanks for asking!" "Feeling fantastic! How can I help you?")
        if "sad" in query or "not well" in query or "bored" in query or "feeling low" in query or "feeling down" in query or "not feeling good" in query:
            speak("I'm here for you. Want to talk about it or should I play some music to cheer you up?")
            #if "talk" in query or "share" in query or "yes" in query:
             #       speak("I'm listening. Tell me what's on your mind.")
             #       speak("Thank you for sharing. Sometimes talking helps. I'm always here for you.")
            if "talk" in query or "share" in query or "i want to talk" in query or "i want to share" in query:
                speak("I'm listening. Tell me what's on your mind.")
                time.sleep(3)  # Give the user time to respond
                response = command()
                if response:
                    speak("Thank you for sharing. Sometimes talking helps. I'm always here for you.")
                else:
                    speak("It's okay if you don't feel like talking now. Just know I'm here whenever you need.")


            elif "play music" in query or "cheer me up" in query:
                speak("Sure! Playing something that might lift your mood.")
                play_music()  # Play music

        elif "play music" in query or "start a song" in query or "I want to hear music" in query or "can you play a song?" in query or "play something" in query or "play some music" in query:
            speak("Sure! Playing something that might lift your m6ood.")
            play_music()  # Play music

        elif ('facebook' in query) or ('discord' in query) or ('whatsapp' in query) or ('instagram' in query):
            social_media(query)
        elif ("university time table" in query) or ("schedule" in query):
            schedule()
        elif ("volume up" in query) or ("increase volume" in query):
            pyautogui.press("volumeup")
            speak("Volume increased")
        elif ("volume down" in query) or ("decrease volume" in query):
            pyautogui.press("volumedown")
            speak("Volume decrease")
        elif ("volume mute" in query) or ("mute the sound" in query):
            pyautogui.press("volumemute")
            speak("Volume muted")
        elif ("open calculator" in query) or ("open notepad" in query) or ("open paint" in query):
            openApp(query)
        elif ("close calculator" in query) or ("close notepad" in query) or ("close paint" in query):
            closeApp(query)
        elif ("hello" in query):
                padded_sequences = pad_sequences(tokenizer.texts_to_sequences([query]), maxlen=20, truncating='post')
                result = model.predict(padded_sequences)
                tag = label_encoder.inverse_transform([np.argmax(result)])

                for i in data['intents']:
                    if i['tag'] == tag:
                        speak(np.random.choice(i['responses']))
#        elif ("open google" in query) or ("open edge" in query):
#           browsing(query)
        elif ("system condition" in query) or ("condition of the system" in query):
            speak("checking the system condition")
            condition()
        elif "weather" in query:
            api_key = "8ef61edcf1c576d65d836254e11ea420"
            base_url = "https://api.openweathermap.org/data/2.5/weather?"
            speak("What's the city name?")
            city_name = command()
            complete_url = base_url + "appid=" + api_key + "&q=" + city_name
            response = requests.get(complete_url)
            x = response.json()
            if x["cod"] != "404":
                y = x["main"]
                current_temperature = y["temp"]
                current_humidity = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                weather_report = f"The temperature in Kelvin is {current_temperature}, Humidity is {current_humidity}%, Weather description is {weather_description}."
                speak(weather_report)
                print(weather_report)
            else:
                speak("City not found")
                print("City not found")

        elif "time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")

        elif "who made you" in query or "who created you" in query or "who discovered you" in query or "who designed you" in query or "who programmed you" in query:
            speak("I was built by Shantika.")
            print("I was built by  Shantika.")

        elif "open stack overflow" in query:
            webbrowser.open_new_tab("https://stackoverflow.com")
            speak("Stack Overflow is open for you")
            time.sleep(5)

        elif "news" in query:
            webbrowser.open_new_tab("https://timesofindia.indiatimes.com/home/headlines")
            speak("Here are some headlines from Times of India. Happy reading!")
            time.sleep(7)

        elif "search" in query:
            query = query.replace("search", "")
            webbrowser.open_new_tab(f"https://www.google.com/search?q={query.strip()}")
            time.sleep(5)

        elif "open youtube" in query:
            webbrowser.open_new_tab("https://www.youtube.com")
            speak("YouTube is open for you")
            time.sleep(5)

        elif "open google" in query:
            webbrowser.open_new_tab("https://www.google.com")
            speak("Google search is open for you")
            time.sleep(5)

        elif "open gmail" in query:
            webbrowser.open_new_tab("https://mail.google.com")
            speak("Gmail is open for you")
            time.sleep(5)

        elif "ask" in query or "can i ask you some questions" in query or "can u answer" in query:
            speak("I can answer to computational and geographical questions. What do you want to ask?")
            question = command()
            app_id = "R2K75H-7ELALHR35X"
            client = wolframalpha.Client(app_id)
            res = client.query(question)
            try:
                answer = next(res.results).text
                speak(answer)
                print(answer)
            except Exception:
                speak("I couldn't find an answer.")


       
        elif "good morning" in query:
            speak("Good morning! I hope you have a productive day ahead.")

        elif "good afternoon" in query:
            speak("Good afternoon! How can I assist you today?")

        elif "good evening" in query:
            speak("Good evening! Hope your day went well.")

        elif "love" in query or "like" in query:
            speak("You are the person who made me and brought me to this wonderful world. Yes, I love you!")

        elif "feel" in query or "feelings" in query:
            speak("Of course! I want to feel your emotions and work with humans.")

        elif "age" in query or "old" in query or "how old are you" in query or "when were you made" in query or "what is your age" in query:
            speak("I am still sweet sixteen, and I will be that forever.")
            query = query.lower()  # convert user input to lowercase for consistent matching

        elif  "hi" in query or "hello" in query or "hey" in query or "hola" in query or "namaste" in query:
            speak("Hi there, how can I help?")

        elif "bye" in query or "see you" in query or "goodbye" in query:
            speak("Bye! Come back again soon.")

        elif "thank" in query or "thanks" in query:
            speak("Happy to help!")

        elif "joke" in query or "make me laugh" in query:
            speak("I ate a clock yesterday, it was very time-consuming.")

        elif ("who are you" in query or "what is your name" in query or "what's your name" in query or "tell me your name" in query or "what can you do" in query or "who is jarvis" in query):
            speak("I am Jarvis, your virtual assistant. I can help you with tasks like checking the weather, searching on Google or Wikipedia, telling jokes, and much more.")

        elif "what's up" in query or "how are you" in query or "sup" in query:
            speak("All good.. What about you?")

        elif "ha ha" in query or "lol" in query or "funny" in query:
            speak("Glad I could make you laugh!")

        elif "dumb" in query or "shut up" in query or "idiot" in query:
            speak("Well that hurts :(")

        elif "what are you doing" in query or "what are you up to" in query:
            speak("Talking to you, of course!")

        elif "awesome" in query or "great" in query or "ok" in query or "yeah" in query or "nice" in query:
            speak("Yeah!")

        elif "you are awesome" in query or "you are great" in query or "you are good" in query:
            speak("Thank you!")

        elif "nice talking" in query or "good talk" in query:
            speak("It was nice talking to you as well! Come back soon!")

        elif "no" in query or "nope" in query:
            speak("Okay!")

        elif "i am good" in query or "i'm fine" in query or "good" in query or "fine" in query:
            speak("Good to know!")

        elif "sad" in query or "not well" in query or "bored" in query or "feeling low" in query:
            speak("I'm here for you. Let me play something to cheer you up.")
    
            music_dir = "C:\\Users\\hp\\Desktop\\jarvisai\\music"  # Change if your folder is elsewhere
            songs = os.listdir(music_dir)

            if songs:
                song = random.choice(songs)
                os.startfile(os.path.join(music_dir, song))
            else:
             speak("Oops, I couldn't find any music files.")

        elif "stop" in query or "goodbye" in query or "ok bye" in query or "see you" in query:
            speak("Your personal AI assistant Jarvis is shutting down, good bye.")
            print("Jarvis is shutting down...")
            break
        elif "exit" in query:
            sys.exit()
        #elif "exit" in query:
            #sys.exit()
# speak("Hello, I'm JARVIS")