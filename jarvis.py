import pygame
import time
import random
import speech_recognition as sr

# Initialize pygame mixer for audio playback
pygame.mixer.init()

# Function to speak text (for your virtual assistant)
def speak(text):
    print(text)  # You can integrate text-to-speech here, like pyttsx3 or gTTS
    # For now, we just print the response to simulate speaking

# Function to play music
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

# Function to recognize speech and convert it to text
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        query = r.recognize_google(audio)
        print(f"You said: {query}")
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
        query = ""
    except sr.RequestError:
        print("There was an issue with the speech service.")
        query = ""

    return query.lower()

# Main code for chatbot interaction
while True:
    # Listening for user query
    query = listen()

    # Checking for certain conditions to respond
    if "sad" in query or "not well" in query or "bored" in query or "feeling low" in query or "feeling down" in query or "not feeling good" in query:
        speak("I'm here for you. Want to talk about it or should I play some music to cheer you up?")
        
        # Check if user wants music to be played
        query = listen()  # Listen for follow-up response

        if "play music" in query or "yes" in query:
            speak("Sure! Playing something that might lift your mood.")
            play_music()  # Play music

    elif "play music" in query or "start a song" in query or "I want to hear music" in query or "can you play a song?" in query or "play something" in query:
        speak("Sure! Playing something that might lift your m6ood.")
        play_music()  # Play music
    
    # Optional: Add more conditions to respond to different types of queries
    elif "exit" in query or "quit" in query:
        speak("Goodbye!")
        break
