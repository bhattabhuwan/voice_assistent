import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from assistant.core import VoiceAssistant
from assistant.gui import AssistantGUI
from threading import Thread, Event
import queue
import time

class AssistantController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.gui = AssistantGUI()
        self.assistant = VoiceAssistant()
        self.command_queue = queue.Queue()
        self.is_listening = False
        self.stop_event = Event()

        # Connect GUI signals
        self.gui.start_listening.connect(self.start_listening)
        self.gui.stop_listening.connect(self.stop_listening)

        # Set up GUI callback for speech
        self.assistant.set_gui_callback(self.gui.add_to_history)

        # Initial greeting
        self.assistant.speak("Hello! I am ZILNOVA, your personal AI assistant. Starting up...")

    def start_listening(self):
        if not self.is_listening:
            self.is_listening = True
            self.stop_event.clear()
            self.gui.update_status("Listening...")
            Thread(target=self.listening_thread, daemon=True).start()
            QTimer.singleShot(500, lambda: self.assistant.speak("I'm listening. How can I help you?"))

    def stop_listening(self):
        if self.is_listening:
            self.is_listening = False
            self.stop_event.set()
            self.gui.update_status("Ready")
            QTimer.singleShot(500, lambda: self.assistant.speak("Voice recognition paused. Click 'Start Listening' when you need me!"))

    def listening_thread(self):
        consecutive_empty = 0
        max_empty = 5  # Maximum number of consecutive empty responses
        
        while self.is_listening and not self.stop_event.is_set():
            try:
                command = self.assistant.listen()
                
                if not command:
                    consecutive_empty += 1
                    if consecutive_empty >= max_empty:
                        self.stop_listening()
                        break
                    continue
                
                consecutive_empty = 0  # Reset counter on valid command
                
                if self.is_listening:
                    self.gui.add_to_history(command, is_user=True)
                    
                    # Check for exit commands
                    if any(word in command.lower() for word in ["exit", "quit", "bye", "goodbye"]):
                        self.stop_listening()
                        self.assistant.speak("Goodbye! ZILNOVA powering down.")
                        self.cleanup()
                        break
                    
                    # Process the command
                    try:
                        self.assistant.process_command(command)
                    except Exception as e:
                        print(f"Error processing command: {str(e)}")
                        self.assistant.speak("I'm sorry, I encountered an error processing that command.")
                    
                    # Small delay to prevent rapid-fire processing
                    time.sleep(0.5)
                    
            except Exception as e:
                print(f"Error in listening thread: {str(e)}")
                self.stop_listening()
                QTimer.singleShot(500, lambda: self.assistant.speak("I encountered an error with voice recognition. Please try again."))
                break

    def cleanup(self):
        """Clean up resources before exiting"""
        self.assistant.shutdown()
        QTimer.singleShot(1000, self.app.quit)

    def run(self):
        self.gui.show()
        # Start listening automatically after 1 second
        QTimer.singleShot(1000, self.start_listening)
        return self.app.exec()

def main():
    controller = AssistantController()
    sys.exit(controller.run())

if __name__ == "__main__":
    main()