import os
import re
import sqlite3
import struct
import threading
import time
import traceback
import webbrowser
from playsound import playsound
import eel
import pvporcupine
import pyaudio
import pyautogui as autogui
from backend.command import speak
from backend.config import ASSISTANT_NAME
import pywhatkit as kit

from backend.helper import extract_yt_term

conn = sqlite3.connect("eryx.db")
cursor = conn.cursor()

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



def PlayYoutube(query):
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
                access_key = "ZMROLjuNfJXo62Phn3A8o36X8nN5Xnna2lXb5mJ7+xvSIQ4/5dtxRg=="  # Replace with your actual access key

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