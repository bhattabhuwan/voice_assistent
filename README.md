# ZILNOVA Voice Assistant

ZILNOVA is a powerful voice assistant built using Python, featuring both voice commands and a modern graphical user interface. It can help you with various tasks like opening applications, checking weather, system monitoring, and more.

## Features

- **Voice Commands**: Natural voice interaction with speech recognition
- **Modern GUI**: Clean and responsive interface with dark theme
- **System Controls**: 
  - Volume control
  - Screenshot capture
  - System monitoring (CPU, Memory, Disk usage)
- **Application Control**:
  - Open common applications (Notepad, Calculator, Paint, etc.)
  - Launch web browsers (Chrome, Edge)
  - Access websites (YouTube, Google, Facebook, etc.)
- **File Management**:
  - Open common folders (Downloads, Documents, Desktop, etc.)
  - File navigation
- **Information Services**:
  - Weather updates
  - Time and date
  - System information

## Project Structure

```
voice-assistant/
├── src/
│   ├── main.py              # Application entry point
│   ├── assistant/           # Core assistant functionality
│   │   ├── __init__.py
│   │   ├── core.py         # Voice assistant logic
│   │   ├── gui.py          # GUI implementation
│   │   ├── icon.png        # Application icon
│   │   └── icon.ico        # Windows icon file
│   └── utils/              # Utility functions
│       └── audio.py        # Audio processing utilities
├── requirements.txt        # Project dependencies
└── README.md              # Documentation
```

## Installation

1. **Clone the repository:**
   ```cmd
   git clone <(https://github.com/bhattabhuwan/voice_assistent)>
   cd voice-assistant
   ```

2. **Create a virtual environment (recommended):**
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```cmd
   pip install -r requirements.txt
   ```

## Usage

1. **Start the application:**
   ```cmd
   python src/main.py
   ```

2. **Using Voice Commands:**
   - Click "Start Listening" to begin voice recognition
   - Speak your command clearly
   - Click "Stop Listening" to pause the assistant

3. **Available Commands:**
   - "Open [application]" - Opens specified application
   - "Open [website]" - Opens specified website
   - "Open folder [name]" - Opens common folders
   - "What's the weather" - Gets weather information
   - "What time is it" - Tells current time
   - "Take a screenshot" - Captures screen
   - "System info" - Shows system status
   - "Volume up/down" - Controls system volume
   - "Help" or "What can you do" - Lists available commands

## Customization

### Adding New Websites
Edit the `urls` dictionary in `core.py` to add new websites:
```python
self.urls = {
    'your_site': 'https://your-site-url.com',
    ...
}
```

### Adding New Applications
Edit the `app_paths` dictionary in `core.py` to add new applications:
```python
app_paths = {
    'app_name': 'path_to_executable',
    ...
}
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Requirements

- Python 3.8 or higher
- Windows OS (some features are Windows-specific)
- Working microphone for voice commands
- Internet connection for weather updates and web features

## License

This project is licensed under the MIT License - see the LICENSE file for details.
# ZILNOVA Voice Assistant

ZILNOVA is an advanced voice assistant with a modern user interface and natural voice interaction capabilities.

## Features

- Voice-controlled interface
- Modern, animated GUI
- Website opening capabilities
- Application launching
- File system navigation
- Natural conversation

## Installation

1. No installation required! Simply download and run `ZILNOVA.exe`
2. On first run, Windows might show a security warning - click "More Info" and then "Run Anyway"

## Voice Commands

- "Open [youtube/facebook/google/gmail]"
- "Open [notepad/calculator/paint]"
- "Open [downloads/documents/desktop] folder"
- "Hello" - Greet ZILNOVA
- "What can you do" - List capabilities
- "Exit" or "Quit" - Close ZILNOVA

## System Requirements

- Windows 10 or later
- Microphone for voice commands
- Speakers or headphones for voice feedback

## Support

For support or to report issues, please contact:bhattabhuwan233@gmail.com

