# Disha Voice Assistant

**Disha** is an English-language voice-controlled virtual assistant built in Python. It combines speech recognition, AI-powered responses via Groq LLaMA 3, and a dynamic GUI for an interactive, real-time experience. Disha can open websites, play music, perform Google/YouTube searches, and answer general questions.

## ✨ Features

- **Voice Activation:** Start the assistant by saying "Hello"
- **Web Navigation:** Open popular websites like Google, YouTube, GitHub, Facebook, and LinkedIn
- **Music Playback:** Play songs directly from YouTube
- **Search Functionality:** Perform Google or YouTube searches via voice commands
- **AI Responses:** Use Groq AI (LLaMA 3) for questions or commands not recognized locally
- **Interactive GUI:**
  - Animated circle with color changes (Idle, Listening, Processing, Error)
  - Halo animation and particle effects for visual feedback
  - Voice amplitude bars reacting to microphone input
- **Multithreaded Design:** Smooth GUI animations and real-time voice processing run in parallel threads
- **Extensible:** Easy to add new commands or music/links

## 📁 Project Structure
```
Disha-Voice-Assistant/
│
├── main.py # Main entry point for the assistant
├── constants.py # Websites, music links, greetings, and config constants
├── interface.py # Tkinter GUI interface
├── .env # Environment variables (API keys, Chrome path)
├── requirements.txt # Python dependencies
└── README.md # Project documentation
```

## 🚀 Setup Instructions

### Prerequisites
- Python ≥ 3.10
- Windows OS (for winsound audio playback)
- Google Chrome installed (for web commands)
- Microphone for voice input

### Installation Steps

#### 1. Clone the Repository
git clone https://github.com/yourusername/Disha-Voice-Assistant.git
cd Disha-Voice-Assistant


#### 2. Install Dependencies
pip install -r requirements.txt


#### 3. Set Up Environment Variables
Create a `.env` file in the root directory:

GROQ_API_KEY=your_groq_api_key_here

CHROME_PATH=C:/Program Files/Google/Chrome/Application/chrome.exe



- **GROQ_API_KEY** → Your personal Groq API key
- **CHROME_PATH** → Full path to Chrome executable on your system

#### 4. Run the Assistant
python main.py


#### 5. Activate the Assistant
Say **"Hello"** to start interacting.

## 🎯 Usage

### Example Voice Commands

| Command | Action |
|---------|--------|
| Open Google | Opens Google in Chrome |
| Open YouTube | Opens YouTube in Chrome |
| Play Shape of You | Plays the song on YouTube |
| Search Python tutorials | Searches Google for Python tutorials |
| Search AI on YouTube | Searches YouTube for AI videos |
| Tell me a joke | AI-generated response via Groq |

*Any command not recognized by the system will be handled by the Groq AI fallback.*

### How It Works

- **Voice Input:** Listens via the microphone and recognizes speech using Google Speech Recognition API
- **Command Parsing:** Commands are matched against predefined keywords (open, play, search)
- **AI Fallback:** Unknown commands are sent to Groq AI for intelligent responses
- **Text-to-Speech:** Uses gTTS to generate natural-sounding audio responses in English
- **GUI Feedback:** Visual feedback through animated circle, halo, particle effects, and voice amplitude bars
- **Multithreading:** Separate threads handle GUI animation and voice processing for smooth real-time interaction

## 📦 Dependencies

- Python ≥ 3.10
- [speechrecognition](https://pypi.org/project/SpeechRecognition/)
- [gTTS](https://pypi.org/project/gTTS/)
- [playsound](https://pypi.org/project/playsound/)
- [numpy](https://pypi.org/project/numpy/)
- [tkinter](https://docs.python.org/3/library/tkinter.html)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [groq](https://pypi.org/project/groq/)

Install all dependencies via:
pip install -r requirements.txt


## 📝 Notes

- The assistant requires an active internet connection for TTS (gTTS) and Groq AI responses
- Works best on Windows for winsound playback
- Chrome must be installed, and the path correctly specified in `.env`

## 🔮 Future Improvements

- Add offline TTS and AI model support
- Extend to multilingual support in future versions
- Include logging and command history
- Develop a web or mobile interface

## 📄 License

MIT License © 2025 [Darshan Surati](https://github.com/Darshan25111)

---

**Made by Darshan Surati**
