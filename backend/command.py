import time
from bs4 import BeautifulSoup
import pyttsx3
import speech_recognition as sr
import eel
from backend.features import *
import datetime
import requests
import keyboard

def speak(text):
    """ Speak the given text using text-to-speech. """
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 130)
    
    eel.DisplaySpokenText(text)
    engine.say(text)
    engine.runAndWait()

    eel.sleep(0.5)  # ✅ Small delay for UI update

    # ✅ Remove `ShowSnake()`, replace with a safe function (if needed)
    try:
        eel.HideListeningShowSiri()  # ✅ Ensure UI resets properly
    except AttributeError:
        print("UI function `HideListeningShowSiri` not found, skipping...")

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        eel.DisplayMessage('Listening...')
        eel.DisplaySpokenText("")
        r.adjust_for_ambient_noise(source, duration=0.5)

        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=20)
            print('Recognizing...')
            eel.DisplayMessage('Recognizing...')
            query = r.recognize_google(audio, language='en-in')
            if query:
                print(f"User said: {query}")
            else:
                print("Sorry, I didn't catch that.")
                eel.ReturnToHomeScreen()
                query = ""  # Return an empty string if nothing is recognized
            eel.DisplaySpokenText(query)
            time.sleep(2)
            return query.lower()

        except sr.WaitTimeoutError:
            eel.DisplayMessage("No speech detected. Try again.")
            return ""  # Return empty string
        except sr.UnknownValueError:
            eel.DisplayMessage("Could not understand audio. Try again.")
            return ""  # Return empty string
        except sr.RequestError:
            eel.DisplayMessage("Network error. Please check your internet connection.")
            return ""  # Return empty string
        except Exception as e:
            print(f"Error: {e}")
            return ""  # Return empty string for any other error


@eel.expose
def allCommands(message=1):
    query = None

    if message == 1:
        query = takecommand()
        print(query)
    else:
        query = message

    # Check for None or empty query
    if not query or query.strip() == "":
        speak("Sorry, I didn't catch that.")
        return

    print("User said:", query)
    query = query.lower()

    try:
        if "volume up" in query:
            try:
                # Simulate pressing volume up key 3 times
                for _ in range(2):
                    keyboard.send("volume up")
                speak("Volume increased")
            except Exception as e:
                print(f"Volume up error: {e}")
                speak("Sorry, I couldn't increase the volume.")

        elif "volume down" in query:
            try:
                # Simulate pressing volume down key 3 times
                for _ in range(2):
                    keyboard.send("volume down")
                speak("Volume decreased")
            except Exception as e:
                print(f"Volume down error: {e}")
                speak("Sorry, I couldn't decrease the volume.")

        elif "i am tired" in query.lower():
            from backend.features import playSpotifyMoodPlaylist
            playSpotifyMoodPlaylist()

        elif "news" in query:
            from backend.features import latestnews
            latestnews()

        elif "screenshot" in query:
            import pyautogui #pip install pyautogui
            im = pyautogui.screenshot()
            im.save("ss.jpg")

        elif "click my photo" in query:
    

            try:
                import subprocess
                import pyautogui
                import time

                speak("Opening camera to take your photo.")
                
                # Open the Windows Camera app
                subprocess.Popen("start microsoft.windows.camera:", shell=True)
                
                # Wait for the camera to fully load
                time.sleep(5)  # You can increase if your PC is slow

                speak("Smile 😊")
                
                # Simulate the spacebar press to take the photo
                pyautogui.press("space")

                speak("Photo clicked!")

                # Optional: Close the camera after 2 seconds
                time.sleep(2)
                pyautogui.hotkey("alt", "f4")

            except Exception as e:
                print(f"[Photo Error] {e}")
                speak("Sorry, I couldn't take your photo.")

        # Check for the "send message" command first to avoid conflicting with greetings
        elif "send message" in query:
            from backend.features import findContact, whatsApp
            message_type = 'message'
            contact_no, name = findContact(query)
            if contact_no is None or name is None:
                speak("Sorry, I couldn't find that contact.")
                return

            if contact_no != 0:
                speak("What message should I send?")
                message_text = takecommand()

                if not message_text or not message_text.strip():
                    speak("I didn't catch the message. Please try again.")
                    return

                whatsApp(contact_no, message_text, message_type, name)

        elif "video call" in query:
            from backend.features import findContact, whatsApp
            message_type = 'video call'
            contact_no, name = findContact(query)
            if contact_no != 0:
                whatsApp(contact_no, "", message_type, name)
                
        elif "call" in query:
            from backend.features import findContact, whatsApp
            message_type = 'call'
            contact_no, name = findContact(query)
            if contact_no != 0:
                whatsApp(contact_no, "", message_type, name)

        
        
        elif "calculator" in query:
            # Open the calculator when the command contains 'calculator'
            # speak("Opening the calculator now.")
            
            # Import open_calculator here, inside the function
            from backend.features import open_calculator
            open_calculator()

        elif "temperature" in query or "weather" in query:
            try:
                import re
                match = re.search(r"(?:in|of)\s+([a-zA-Z\s]+)", query)
                city = match.group(1).strip() if match else "delhi"

                url = f"https://wttr.in/{city}?format=%t+%C"
                headers = {
                    "User-Agent": "curl/7.64.1"
                }

                response = requests.get(url, headers=headers)

                if response.status_code == 200:
                    weather = response.text.strip()
                    speak(f"The current temperature and condition in {city} is {weather}")
                else:
                    speak(f"Sorry, I couldn't fetch the weather for {city}. Try again later.")
            except Exception as e:
                print(f"[Weather Error] {e}")
                speak("There was a problem getting the temperature.")

        # Now handle greetings after more specific commands like sending messages
        elif any(phrase in query for phrase in ["hello", "hi", "hey"]):
            speak("Hello , how are you?")

        elif "i am fine" in query or "i'm fine" in query:
            speak("That's great!")

        elif "how are you" in query:
            speak("Perfect!")

        elif "thank you" in query or "thanks" in query:
            speak("You're welcome.")

        elif "open" in query:
            from backend.features import opencommand
            opencommand(query)
        elif "close" in query:
            from backend.features import closecommand
            closecommand(query)

        elif "on youtube" in query:
            from backend.features import PlayYoutube
            PlayYoutube(query)
        elif "google" in query:
            from backend.features import searchGoogle
            searchGoogle(query)
        elif "wikipedia" in query:
            from backend.features import searchWikipedia
            searchWikipedia(query)
        

        elif "time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M")    
            speak(f"The time is {strTime}")

        # if 'clock' in query or 'alarm' in query:
        #     from backend.features import open_clock
        #     open_clock()


        else:
            print("Command not recognized.")

    except Exception as e: 
        print(f"Error: {e}")

    eel.AssistantFinished()
    eel.HideListeningShowSiri()