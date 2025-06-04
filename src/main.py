import speech_recognition as sr
import pyttsx3
from assistant.core import VoiceAssistant

def main():
    assistant = VoiceAssistant()
    assistant.start()

if __name__ == "__main__":
    main()