import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import subprocess
import datetime
import json
import psutil
import requests
import pyautogui
from typing import Dict, Any
from queue import Queue
from threading import Thread, Lock, Event
import time

class VoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = None
        self.speech_queue = Queue()
        self.speech_thread = None
        self.speech_lock = Lock()
        self.stop_speech = Event()
        self.gui_callback = None
        
        # Developer information
        self.developer_info = {
            "name": "Bhuwan Bhatt",
            "role": "AI and Software Developer",
            "specialization": "Voice Assistant and AI Systems",
            "location": "India",
            "project": "ZILNOVA AI Assistant"
        }
        
        # Initialize speech thread
        self._init_speech_engine()
        self.start_speech_thread()
        
        # Initialize commands
        self.commands = {
            'hello': self._handle_greeting,
            'hi': self._handle_greeting,
            'hey': self._handle_greeting,
            'time': self._handle_time,
            'date': self._handle_date,
            'weather': self._handle_weather,
            'help': self._handle_help,
            'what can you do': self._handle_help,
            'system info': self._handle_system_info,
            'screenshot': self._handle_screenshot,
            'who created you': self._handle_creator_info,
            'who made you': self._handle_creator_info,
            'who is your creator': self._handle_creator_info,
            'who developed you': self._handle_creator_info,
            'about developer': self._handle_creator_info,
            'tell me about yourself': self._handle_self_intro,
            'introduce yourself': self._handle_self_intro,
        }
        
        # URLs for web commands
        self.urls = {
            'youtube': 'https://www.youtube.com',
            'google': 'https://www.google.com',
            'gmail': 'https://mail.google.com',
            'github': 'https://github.com',
            'facebook': 'https://www.facebook.com',
            'twitter': 'https://twitter.com',
            'linkedin': 'https://www.linkedin.com',
            'amazon': 'https://www.amazon.com'
        }
        
        # Applications
        self.apps = {
            'notepad': 'notepad.exe',
            'calculator': 'calc.exe',
            'paint': 'mspaint.exe',
            'word': 'winword.exe',
            'excel': 'excel.exe'
        }

    def _init_speech_engine(self):
        """Initialize the text-to-speech engine"""
        try:
            self.engine = pyttsx3.init()
            voices = self.engine.getProperty('voices')
            # Try to set a female voice if available
            for voice in voices:
                if "female" in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    break
            self.engine.setProperty('rate', 150)    # Speed of speech
            self.engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)
        except Exception as e:
            print(f"Error initializing speech engine: {str(e)}")

    def start_speech_thread(self):
        """Start the speech processing thread"""
        if not self.speech_thread or not self.speech_thread.is_alive():
            self.speech_thread = Thread(target=self._process_speech_queue, daemon=True)
            self.speech_thread.start()

    def _process_speech_queue(self):
        """Process queued speech items"""
        while not self.stop_speech.is_set():
            try:
                if not self.speech_queue.empty():
                    text = self.speech_queue.get()
                    if text:
                        # Update GUI first
                        if self.gui_callback:
                            self.gui_callback(text)
                        # Then speak
                        with self.speech_lock:
                            if self.engine is None:
                                self._init_speech_engine()
                            print(f"ZILNOVA: {text}")
                            self.engine.say(text)
                            self.engine.runAndWait()
                    self.speech_queue.task_done()
            except Exception as e:
                print(f"Error in speech thread: {str(e)}")
                # Reinitialize the engine if there's an error
                self._init_speech_engine()

    def set_gui_callback(self, callback):
        """Set the GUI callback function"""
        self.gui_callback = callback

    def speak(self, text: str):
        """Add text to speech queue"""
        if text and isinstance(text, str):
            self.speech_queue.put(text.strip())

    def shutdown(self):
        """Cleanup speech resources"""
        self.stop_speech.set()
        if self.speech_thread and self.speech_thread.is_alive():
            self.speech_thread.join(timeout=1)
        with self.speech_lock:
            if self.engine:
                try:
                    self.engine.stop()
                except:
                    pass

    def listen(self):
        """Listen for voice input with improved error handling"""
        try:
            with sr.Microphone() as source:
                print("Listening...")
                # Adjust for ambient noise and set timeout
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                self.recognizer.dynamic_energy_threshold = True
                
                try:
                    # Wait for speech with timeout
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    
                    # Convert speech to text
                    text = self.recognizer.recognize_google(audio).lower()
                    print(f"Heard: {text}")
                    return text
                except sr.WaitTimeoutError:
                    return ""
                except sr.UnknownValueError:
                    return ""
                except sr.RequestError:
                    print("Could not request results from speech recognition service")
                    return ""
        except Exception as e:
            print(f"Error in listen(): {str(e)}")
            return ""

    def process_command(self, command: str) -> None:
        """Process voice commands"""
        try:
            command = command.lower().strip()
            
            # Check for basic commands
            for key, handler in self.commands.items():
                if key in command:
                    handler(command)
                    return

            # Only provide help when specifically asked
            if any(word in command for word in ["help", "what can you do", "instructions", "guide me"]):
                self._handle_help(command)
                return
                    
            # Handle open commands
            if any(word in command for word in ["open", "launch", "start", "run"]):
                self._handle_open_command(command)
                return
                
            # Simple response for unrecognized commands
            self.speak("I didn't understand that command. Say 'help' if you need assistance.")
            
        except Exception as e:
            print(f"Error processing command: {str(e)}")
            self.speak("Sorry, I encountered an error. Please try again.")

    def _handle_open_command(self, command: str) -> None:
        """Handle open/launch commands"""
        try:
            # Website commands
            for site, url in self.urls.items():
                if site in command:
                    self.speak(f"Opening {site}")
                    webbrowser.open(url)
                    return
            
            # Application commands
            for app_name, app_exec in self.apps.items():
                if app_name in command:
                    try:
                        subprocess.Popen(app_exec)
                        self.speak(f"Opening {app_name}")
                    except FileNotFoundError:
                        self.speak(f"Sorry, I couldn't find {app_name}")
                    return
            
            self.speak("Please specify which website or application you want to open.")
            
        except Exception as e:
            print(f"Error opening application/website: {str(e)}")
            self.speak("Sorry, I couldn't open that.")

    def _handle_greeting(self, command: str) -> None:
        """Handle greeting commands"""
        greetings = [
            "Hello! How can I help you today?",
            "Hi there! What can I do for you?",
            "Hello! I'm here to assist you.",
            "Hey! How can I be of service?"
        ]
        import random
        self.speak(random.choice(greetings))

    def _handle_time(self, command: str) -> None:
        """Handle time-related commands"""
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        self.speak(f"The current time is {current_time}")

    def _handle_date(self, command: str) -> None:
        """Handle date-related commands"""
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        self.speak(f"Today's date is {current_date}")

    def _handle_system_info(self, command: str) -> None:
        """Handle system information requests"""
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        info = (
            f"Here's your system status:\n"
            f"CPU usage is {cpu}%\n"
            f"Memory usage is {memory.percent}%\n"
            f"Disk usage is {disk.percent}%"
        )
        self.speak(info)

    def _handle_screenshot(self, command: str) -> None:
        """Handle screenshot requests"""
        try:
            # Generate filename with timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = os.path.expanduser(f"~/Desktop/screenshot_{timestamp}.png")
            pyautogui.screenshot(screenshot_path)
            self.speak(f"Screenshot taken and saved to your desktop as screenshot_{timestamp}.png")
        except Exception as e:
            print(f"Screenshot error: {str(e)}")
            self.speak("Sorry, I couldn't take a screenshot")

    def _handle_creator_info(self, command: str) -> None:
        """Handle questions about the creator/developer"""
        creator_response = (
            f"I was created by {self.developer_info['name']}, "
            f"who is an {self.developer_info['role']} specializing in {self.developer_info['specialization']}. "
            f"He developed me as an advanced AI assistant to help users with various tasks. "
            f"I'm proud to be part of his innovative work in AI technology."
        )
        self.speak(creator_response)
        
    def _handle_self_intro(self, command: str) -> None:
        """Handle self-introduction requests"""
        intro = (
            f"I am ZILNOVA, an AI assistant developed by {self.developer_info['name']}. "
            "I can help you with various tasks like checking the weather, managing your computer, "
            "opening applications and websites, and providing system information. "
            "I'm designed to be your helpful digital companion, always ready to assist you "
            "with both simple and complex tasks. Feel free to ask me anything!"
        )
        self.speak(intro)

    def _handle_help(self, command: str) -> None:
        """Handle help commands with concise information"""
        help_text = (
            "Here are my main commands:\n"
            "- Basic: hello, time, date\n"
            "- Open: websites (YouTube, Google, etc.) or apps (Notepad, Calculator)\n"
            "- System: system info, screenshot\n"
            "- Other: weather, about developer"
        )
        self.speak(help_text)

    def _handle_weather(self, command: str) -> None:
        """Handle weather-related commands"""
        try:
            # Extract city name from command
            city = "London"  # default city
            command = command.lower()
            
            if "in" in command:
                # Try to extract city name after "in"
                city = command.split("in")[-1].strip()
            elif "at" in command:
                # Try to extract city name after "at"
                city = command.split("at")[-1].strip()
            elif "for" in command:
                # Try to extract city name after "for"
                city = command.split("for")[-1].strip()
            
            # Remove any extra words that might have been captured
            city = city.split()[0] if city.split() else "London"
            
            if not self.weather_api_key or self.weather_api_key == "YOUR_API_KEY":
                self.speak("I apologize, but I haven't been configured with a weather API key yet. "
                         "You'll need to add an OpenWeatherMap API key to use this feature.")
                return
                
            # Make API request
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.weather_api_key}&units=metric"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                temp = data['main']['temp']
                weather_desc = data['weather'][0]['description']
                humidity = data['main']['humidity']
                
                weather_info = (
                    f"The weather in {city} is {weather_desc} with a temperature of "
                    f"{temp:.1f}°C and humidity of {humidity}%"
                )
                self.speak(weather_info)
            else:
                self.speak(f"I'm sorry, I couldn't find weather information for {city}")
                
        except requests.RequestException:
            self.speak("I'm having trouble connecting to the weather service. Please check your internet connection.")
        except Exception as e:
            print(f"Weather error: {str(e)}")
            self.speak("I'm sorry, I encountered an error while getting the weather information.")
