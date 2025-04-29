import os
import random
import sqlite3
import struct
import subprocess
import threading
import time
import traceback
import webbrowser
from playsound import playsound
import eel
import pvporcupine
import pyaudio
import pyautogui as autogui
import requests
import speech_recognition as sr
from backend.command import speak
from backend.config import ASSISTANT_NAME
import wikipedia
import pyttsx3
import pygetwindow as gw
import urllib


from backend.helper import extract_yt_term, remove_words

conn = sqlite3.connect("eryx.db")
cursor = conn.cursor()
engine = pyttsx3.init()
@eel.expose
def playAssistantSound():
    """ Play assistant startup sound """
    music_dir = "frontend\\assets\\audio\\audio1.mp3"
    playsound(music_dir)

def opencommand(query):
    """ Opens applications based on user voice command """
    query = query.replace(ASSISTANT_NAME, "").strip()
    query = query.replace("open", "").strip().lower()

    app_name = query.strip()
    print(f"Received command: {app_name}")

    if app_name in ["alarm", "clock"]:
        try:
            speak("Opening Clock")
            os.system("start ms-clock:")
            print("Clock app launched.")
        except Exception as e:
            print("Error launching clock:", e)
            speak("Sorry, I couldn't open the clock.")
        return  # Important to stop further execution

    # Create a new SQLite connection inside the function
    conn = sqlite3.connect("eryx.db")
    cursor = conn.cursor()

    if app_name:
        try:
            cursor.execute('SELECT path FROM sys_command WHERE name = ?', (app_name,))
            results = cursor.fetchall()
            print(f"DB results (sys_command): {results}")

            if results:
                speak("Opening " + query)
                os.startfile(results[0][0])
            else:
                cursor.execute('SELECT url FROM web_command WHERE name = ?', (app_name,))
                results = cursor.fetchall()
                print(f"DB results (web_command): {results}")

                if results:
                    speak("Opening " + query)
                    webbrowser.open(results[0][0])
                else:
                    # Special case for YouTube
                    if "youtube" in app_name:
                        speak("Opening YouTube")
                       
                        webbrowser.open("https://www.youtube.com")
                    else:
                        speak("Opening " + query)
                        try:
                            print(f"Executing: os.system('start {query}')")
                            os.system(f'start {query}')
                        except Exception as e:
                            print(f"Error: {e}")
                            speak("Application not found.")
        except Exception as e:
            print(f"SQL Error: {e}")
            speak("Something went wrong")
        finally:
            conn.close()  # Ensure the connection is closed properly
            

def close_window_with_title(query):
    found = False
    for window in gw.getAllTitles():
        if query.lower() in window.lower() and window.strip() != "":
            print(f"Found matching window: {window}")
            win = gw.getWindowsWithTitle(window)[0]
            win.close()
            found = True
            print(f"Closed window: {window}")
            engine.say(f"Closed {query}")
            engine.runAndWait()
            break
    if not found:
        print(f"No open window found for: {query}")
        engine.say(f"No open window found for {query}")
        engine.runAndWait()

def closecommand(query):
    name = query.replace("close", "").strip().lower()
    print(f"Looking for windows with: {name}")

    windows = gw.getAllTitles()
    for w in windows:
        print(f"Found window: {w}")  # 🔍 Print all open window titles
    
    found = False
    for window in gw.getWindowsWithTitle(name):
        print(f"Closing window: {window.title}")
        window.close()
        found = True
        

    if not found:
        print(f"No open window found for: {name}")

def PlayYoutube(query):
    import pywhatkit as kit
    search_term = extract_yt_term(query)
    speak("Playing "+search_term+" on YouTube")
    kit.playonyt(search_term)


def hotword():
    class HotwordDetector:
        def __init__(self):
            self.porcupine = None
            self.paud = None
            self.audio_stream = None
            self.running = True  # Control loop execution

        def start(self):
            try:
                print("Initializing Hotword Detector...")
                access_key = "l1dEfraxGosyk1c6rCVuKJIKPbteE/xApZyUpeme0cVAeajR8WnsZA=="  # Replace with your actual access key

                # Load Porcupine wake word detection
                self.porcupine = pvporcupine.create(
                    access_key=access_key,
                    keyword_paths=[r"D:\Project-6th sem\ERYX\eryx_en_windows_v3_0_0.ppn"],
                    sensitivities=[0.95]  # High sensitivity
                )

                self.paud = pyaudio.PyAudio()
                self.audio_stream = self.paud.open(
                    rate=self.porcupine.sample_rate,
                    channels=1,
                    format=pyaudio.paInt16,
                    input=True,
                    frames_per_buffer=self.porcupine.frame_length,
                    stream_callback=self.callback
                )

                print("Listening for 'Eryx' hotword...")
                self.audio_stream.start_stream()

                while self.running:
                    time.sleep(0.1)  # Keeps script running while reducing CPU usage

            except Exception as e:
                print(f"Error: {e}")
                with open("error_log.txt", "w") as f:
                    f.write(traceback.format_exc())  # Log errors

            finally:
                self.cleanup()

        def callback(self, in_data, frame_count, time_info, status):
            try:
                keyword = struct.unpack_from("h" * self.porcupine.frame_length, in_data)
                keyword_index = self.porcupine.process(keyword)

                if keyword_index >= 0:
                    print("Hotword 'Eryx' detected! Triggering shortcut...")

                    # Trigger Ctrl + Shift + E
                    autogui.hotkey("ctrl", "shift", "e")

            except Exception as e:
                print(f"Callback Error: {e}")
                with open("error_log.txt", "a") as f:
                    f.write(traceback.format_exc())  # Log errors

            return (in_data, pyaudio.paContinue)

        def stop(self):
            self.running = False

        def cleanup(self):
            if self.porcupine:
                self.porcupine.delete()
            if self.audio_stream:
                self.audio_stream.stop_stream()
                self.audio_stream.close()
            if self.paud:
                self.paud.terminate()
            print("Stopped listening.")

    # Start Hotword Detection in a separate thread
    try:
        detector = HotwordDetector()
        thread = threading.Thread(target=detector.start, daemon=True)
        thread.start()

        while True:
            command = input("Type 'exit' to stop: ").strip().lower()
            if command == "exit":
                detector.stop()
                break

    except Exception as e:
        with open("error_log.txt", "w") as f:
            f.write(traceback.format_exc())  # Log startup errors


# Whatsapp Message Sending
def findContact(query):
    import sqlite3

    # Remove unnecessary words from the query
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()

        # Use a fresh SQLite connection to avoid threading issues
        conn = sqlite3.connect('eryx.db')
        cursor = conn.cursor()

        # Search for contact using case-insensitive query
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()

        conn.close()  # Close the DB connection properly

        if results:
            mobile_number_str = str(results[0][0])
            if not mobile_number_str.startswith('+91'):
                mobile_number_str = '+91' + mobile_number_str

            return mobile_number_str, query
        else:
            speak('not exist in contacts')
            return 0, 0

    except Exception as e:
        speak('not exist in contacts')
        print("Database error:", e)
        return 0, 0

def whatsApp(mobile_no, message, flag, name):
    if mobile_no is None or name is None:
        print("Invalid contact details. Aborting WhatsApp action.")
        return

    try:
        # Encode the message
        encoded_message = urllib.parse.quote(message)

        # Open WhatsApp chat
        whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"
        webbrowser.open(whatsapp_url)

        time.sleep(5)  # Wait for WhatsApp chat to load

        if flag == 'message':
            autogui.press('enter')  # Press Enter to send the message
            speak(f"Message sent successfully to {name}")

        elif flag == 'call':
            # Locate the Call button on screen
            call_location = autogui.locateCenterOnScreen("D:/Project-6th sem/ERYX/frontend/assets/call_button.png", confidence=0.8)
            if call_location:
                autogui.moveTo(call_location, duration=0.5)
                autogui.click()
                speak(f"Calling {name}")
            else:
                speak("Couldn't find the Call button.")

        elif flag == 'video call':
            # Locate the Video Call button on screen
            video_call_location = autogui.locateCenterOnScreen("D:/Project-6th sem/ERYX/frontend/assets/video_call_button.png", confidence=0.8)
            if video_call_location:
                autogui.moveTo(video_call_location, duration=0.5)
                autogui.click()
                speak(f"Starting video call with {name}")
            else:
                speak("Couldn't find the Video Call button.")

    except Exception as e:
        print(f"WhatsApp launch error: {e}")
        traceback.print_exc()
        speak("Couldn't complete the WhatsApp action.")


from datetime import datetime
from backend.command import speak

def greetMe():
    hour = int(datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good morning! I am Eryx, your desktop assistant.")
    elif 12 <= hour < 18:
        speak("Good afternoon! I am Eryx, your desktop assistant.")
    else:
        speak("Good evening! I am Eryx, your desktop assistant.")

def searchGoogle(query):
    import pywhatkit
    if "google" in query:
        import wikipedia as googleScrap
        query = query.replace("eryx","")
        query = query.replace("google search","")
        query = query.replace("google","")
        speak("This is what I found on google")

        try:
            pywhatkit.search(query)
            result = googleScrap.summary(query,1)
            speak(result)

        except:
            speak("No speakable output available")

import wikipedia
import webbrowser

def searchWikipedia(query):
    if "wikipedia" in query:
        speak("Searching from Wikipedia...")
        query = query.replace("wikipedia", "")
        query = query.replace("search wikipedia", "")
        query = query.replace("eryx", "")
        query = query.strip()

        try:
            results = wikipedia.summary(query, sentences=2)
            page = wikipedia.page(query)
            speak("According to Wikipedia...")
            # Open the specific Wikipedia page
            webbrowser.open(page.url)
            print(results)
            speak(results)
            
            

        except wikipedia.exceptions.DisambiguationError as e:
            speak("There are multiple results. Please be more specific.")
            print("DisambiguationError:", e)
        except wikipedia.exceptions.PageError:
            speak("Sorry, I couldn't find anything matching that.")
            print("PageError: No matching page found.")

def open_clock():
    try:
        os.system("start ms-clock:")
        print("Clock app launched.")
    except Exception as e:
        print("Error launching clock:", e)


def playSpotifyMoodPlaylist():
    try:
        subprocess.Popen("spotify")  # Launch Spotify
        speak("Playing your favourite playlist to help you relax, Enjoy!")
        time.sleep(2)  # Let Spotify launch

        # Open the playlist in default browser (should redirect to app)
        webbrowser.open("https://open.spotify.com/playlist/0kComKjmca3ZT8cugeBWm3")
        time.sleep(2)

        # Enable shuffle (ctrl + s is the shortcut)
        autogui.hotkey("ctrl", "s")
        time.sleep(1)

        # Scroll down randomly to reach deeper songs (optional)
        for _ in range(random.randint(10, 20)):
            autogui.press("down")
            time.sleep(0.1)

        # Random click within the playlist song area
        # Adjust these x, y values for your screen to stay on the song column
        x = random.randint(200, 500)  # X-range within the left half of playlist (song titles)
        y = random.randint(400, 600)  # Y-range covering the playlist song rows

        # Move to the random song and click
        autogui.click(x, y)
        time.sleep(1)

        # Just to make sure, press Enter again to play the song
        autogui.press("enter")
        time.sleep(1)

        # speak("Playing a random song from your playlist.")

    except Exception as e:
        print(f"Error: {e}")
        speak("Something went wrong while playing music.")





def open_calculator():
    """ Open the calculator application. """
    try:
        os.system('start calc')  # This will open the default calculator on Windows
        speak("Opening the calculator now.")
    except Exception as e:
        print(f"Error opening calculator: {e}")
        speak("Sorry, I couldn't open the calculator.")


def takecommand(prompt=""):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        if prompt:
            speak(prompt)
        print("Adjusting for ambient noise... Please wait.")
        r.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        try:
            audio = r.listen(source, timeout=6, phrase_time_limit=7)
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
            return query.lower()
        except sr.WaitTimeoutError:
            print("Listening timed out.")
            return ""
        except sr.UnknownValueError:
            print("Speech unclear.")
            return ""
        except sr.RequestError:
            print("Speech recognition service unavailable.")
            return ""
        except Exception as e:
            print(f"Error: {e}")
            return ""

def latestnews():
    api_dict = {
        "business": "https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey=11fe423d162d4d5b9b5294cb6e499501",
        "entertainment": "https://newsapi.org/v2/top-headlines?country=in&category=entertainment&apiKey=11fe423d162d4d5b9b5294cb6e499501",
        "health": "https://newsapi.org/v2/top-headlines?country=in&category=health&apiKey=11fe423d162d4d5b9b5294cb6e499501",
        "science": "https://newsapi.org/v2/top-headlines?country=in&category=science&apiKey=11fe423d162d4d5b9b5294cb6e499501",
        "sports": "https://newsapi.org/v2/top-headlines?country=in&category=sports&apiKey=11fe423d162d4d5b9b5294cb6e499501",
        "technology": "https://newsapi.org/v2/top-headlines?country=in&category=technology&apiKey=11fe423d162d4d5b9b5294cb6e499501"
    }

    url = None
    # category_list = ", ".join(api_dict.keys())

    # Ask 3 times for category
    for attempt in range(3):
        field = takecommand(f"Which category of news do you want?")
        if not field:
            speak("Sorry, I didn't hear anything.")
            continue

        for key in api_dict:
            if key in field:
                url = api_dict[key]
                print(f"Matched category: {key}")
                break

        if url:
            break
        else:
            speak("I didn't recognize that category. Please try again.")

    if not url:
        speak("Still couldn't understand the category. Please try again later.")
        return

    try:
        response = requests.get(url)
        news = response.json()
        articles = news.get("articles", [])
        if not articles:
            speak("Sorry, no news found.")
            return

        speak("Here are the latest headlines.")
        for i, article in enumerate(articles[:5]):
            title = article.get("title", "No Title")
            link = article.get("url", "")
            print(f"{i+1}. {title}")
            print(f"More info: {link}")
            speak(f"News {i+1}: {title}")
            time.sleep(1)

        speak("That’s all for now.")
    except Exception as e:
        print(f"Error fetching news: {e}")
        speak("There was a problem getting the news.")