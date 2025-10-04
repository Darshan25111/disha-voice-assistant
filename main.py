import os
import webbrowser
import threading
import time
import speech_recognition as sr
from gtts import gTTS
from dotenv import load_dotenv
from groq import Groq
import constants
from interface import DishaInterface  # Import your interface
import playsound
import winsound

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
CHROME_PATH = os.getenv("CHROME_PATH")
chrome = webbrowser.get(f'"{CHROME_PATH}" %s')

# --- Safe Text-to-Speech ---
def speak(text, gui=None):
    print("🗣️ Disha:", text)
    if gui: gui.set_status(text)
    tts = gTTS(text=text, lang='en')
    mp3_file = "voice.mp3"
    wav_file = "voice.wav"
    tts.save(mp3_file)

    # Convert mp3 -> wav
    try:
        os.system(f'ffmpeg -y -i {mp3_file} {wav_file} >nul 2>&1')
        if os.path.exists(wav_file):
            winsound.PlaySound(wav_file, winsound.SND_FILENAME)
            os.remove(wav_file)
        else:
            playsound.playsound(mp3_file)
    except:
        playsound.playsound(mp3_file)
    finally:
        if os.path.exists(mp3_file):
            os.remove(mp3_file)

# --- AI fallback ---
def aiProcess(command, context=None):
    client = Groq(api_key=GROQ_API_KEY)
    messages = [{"role": "system", "content": "You are a virtual assistant named Disha. Keep responses short and clear."}]
    if context:
        messages.extend(context)
    messages.append({"role": "user", "content": command})
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=messages
    )
    return completion.choices[0].message.content

# --- Command handler ---
def processCommand(command, context=None, gui=None):
    command = command.lower()
    if gui: gui.set_processing(True)

    if command.startswith("open "):
        site = command.replace("open ", "").strip()
        url = constants.LINKS.get(site)
        if url:
            chrome.open(url)
            speak(f"Opening {site}", gui)
        else:
            speak("I don't know that site.", gui)

    elif command.startswith("play "):
        song = command.replace("play ", "").strip()
        link = constants.MUSIC.get(song)
        if link:
            chrome.open(link)
            speak(f"Playing {song}", gui)
        else:
            speak("I couldn't find that song.", gui)

    elif command.startswith("search "):
        query = command.replace("search ", "").strip()
        if "youtube" in query:
            query = query.replace("on youtube", "").strip()
            url = constants.YOUTUBE_BASE + query.replace(" ", "+")
            chrome.open(url)
            speak(f"Searching YouTube for {query}", gui)
        else:
            url = constants.GOOGLE_BASE + query.replace(" ", "+")
            chrome.open(url)
            speak(f"Searching Google for {query}", gui)

    else:
        output = aiProcess(command, context)
        speak(output, gui)
        if context is None: context = []
        context.append({"role": "user", "content": command})
        context.append({"role": "assistant", "content": output})

    if gui: gui.set_listening(True)
    return context

# --- Listen and respond ---
def listen_and_respond(gui=None, context=None, duration=30):
    recognizer = sr.Recognizer()
    start_time = time.time()

    if gui: gui.set_listening(True)

    while time.time() - start_time < duration:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=6)
                command = recognizer.recognize_google(audio)
                print("✅ You said:", command)
                context = processCommand(command, context, gui)
                start_time = time.time()
        except sr.WaitTimeoutError:
            pass
        except sr.UnknownValueError:
            pass
        except sr.RequestError:
            pass
        except Exception as e:
            print(f"⚠️ {e}")

    if gui: gui.set_status("Idle")
    return context

# --- Assistant main loop ---
def assistant_main(gui):
    speak(constants.DEFAULT_GREETING, gui)
    recognizer = sr.Recognizer()
    context = []

    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=3)
                keyword = recognizer.recognize_google(audio).lower()
                if keyword == "hello":
                    speak("Yes Boss! How can I assist you?", gui)
                    context = listen_and_respond(gui, context)
        except:
            continue

# --- Main ---
if __name__ == "__main__":
    gui = DishaInterface()

    # Run assistant logic in background
    threading.Thread(target=assistant_main, args=(gui,), daemon=True).start()

    # Start GUI loop
    gui.start()
