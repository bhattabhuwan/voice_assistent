import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import subprocess

class VoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        # Set voice properties
        voices = self.engine.getProperty('voices')
        # Try to set a female voice if available
        for voice in voices:
            if "female" in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
        self.engine.setProperty('rate', 150)  # Speed of speech
        self.is_listening = False
        # Define common paths and URLs
        self.urls = {
            'youtube': 'https://www.youtube.com',
            'facebook': 'https://www.facebook.com',
            'google': 'https://www.google.com',
            'gmail': 'https://mail.google.com'
        }

    def listen(self):
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = self.recognizer.listen(source)
            try:
                text = self.recognizer.recognize_google(audio)
                print(f"You said: {text}")
                return text.lower()
            except sr.UnknownValueError:
                return ""
            except sr.RequestError:
                self.speak("I'm having trouble connecting to my speech service.")
                return ""

    def speak(self, text):
        print(f"ZILNOVA: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def open_website(self, site):
        if site in self.urls:
            self.speak(f"Opening {site}")
            webbrowser.open(self.urls[site])
        else:
            self.speak(f"Sorry, I don't have {site} in my list of websites")

    def open_folder(self, path):
        try:
            os.startfile(path)
            self.speak(f"Opening folder: {path}")
        except:
            self.speak("Sorry, I couldn't find that folder")

    def open_application(self, app_name):
        try:
            if app_name == "notepad":
                subprocess.Popen("notepad.exe")
            elif app_name == "calculator":
                subprocess.Popen("calc.exe")
            elif app_name == "paint":
                subprocess.Popen("mspaint.exe")
            else:
                self.speak(f"Sorry, I don't know how to open {app_name}")
                return
            self.speak(f"Opening {app_name}")
        except Exception as e:
            self.speak(f"Sorry, I couldn't open {app_name}")

    def start(self):
        self.is_listening = True
        self.speak("Hello, I am ZILNOVA, your personal AI assistant. How may I assist you?")
        while self.is_listening:
            command = self.listen()
            if command:
                if "exit" in command or "quit" in command:
                    self.speak("Goodbye! ZILNOVA powering down.")
                    self.is_listening = False
                    break
                elif "hello" in command or "hi" in command:
                    self.speak("Hello! I'm ZILNOVA. How can I help you today?")
                elif "what can you do" in command:
                    self.speak("I can help you open websites, applications, and folders. Just tell me what you'd like to open.")
                
                # Handle opening websites
                elif "open youtube" in command:
                    self.open_website("youtube")
                elif "open facebook" in command:
                    self.open_website("facebook")
                elif "open google" in command:
                    self.open_website("google")
                elif "open gmail" in command:
                    self.open_website("gmail")
                
                # Handle opening applications
                elif "open notepad" in command:
                    self.open_application("notepad")
                elif "open calculator" in command:
                    self.open_application("calculator")
                elif "open paint" in command:
                    self.open_application("paint")
                
                # Handle opening folders
                elif "open folder" in command:
                    if "downloads" in command.lower():
                        self.open_folder(os.path.expanduser("~/Downloads"))
                    elif "documents" in command.lower():
                        self.open_folder(os.path.expanduser("~/Documents"))
                    elif "desktop" in command.lower():
                        self.open_folder(os.path.expanduser("~/Desktop"))
                    else:
                        self.speak("Please specify which folder to open.")
                
                else:
                    self.speak("I heard you say: " + command + ". How can I help with that?")