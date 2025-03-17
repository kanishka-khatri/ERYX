import time
import pyttsx3
import speech_recognition as sr
import eel

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
    """ Recognize voice input and return the recognized text. """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        eel.DisplayMessage('Listening...')
        eel.DisplaySpokenText("")  # ✅ Clear previous text
        r.adjust_for_ambient_noise(source, duration=0.5)

        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=20)
            print('Recognizing...')
            eel.DisplayMessage('Recognizing...')
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
            eel.DisplaySpokenText(query)
            time.sleep(2)
            return query.lower()  # ✅ Return text without speaking it

        except sr.WaitTimeoutError:
            eel.DisplayMessage("No speech detected. Try again.")
        except sr.UnknownValueError:
            eel.DisplayMessage("Could not understand audio. Try again.")
        except sr.RequestError:
            eel.DisplayMessage("Network error. Please check your internet connection.")
    return ""

@eel.expose
def allCommands():

    try:
        query = takecommand()
        print(query)

        if "open" in query:
            from backend.features import opencommand
            opencommand(query)
        elif "on youtube":
            from backend.features import PlayYoutube 
            PlayYoutube(query)
        else:
            print("Command not recognized.")

    except:
        print("Error.")

    eel.AssistantFinished()  # ✅ Ensure UI resets after execution
    # eel.ShowSnake()
    eel.HideListeningShowSiri()  # ✅ Hide Listening GIF & Show Siri Wave
    eel.AssistantFinished()  # ✅ Ensure UI resets even on failure