# import struct
# import time
# import pvporcupine
# import pyaudio
# import pyautogui as autogui

# def hotword():
#     porcupine = None
#     paud = None
#     audio_stream = None
#     try:
#         # Replace 'YOUR_ACCESS_KEY' with your actual Picovoice access key
#         access_key = "ZMROLjuNfJXo62Phn3A8o36X8nN5Xnna2lXb5mJ7+xvSIQ4/5dtxRg=="

#         # Provide the path to your "hey eryx" PPN file
#         porcupine = pvporcupine.create(
#             access_key=access_key,
#             keyword_paths=[r"D:\Project-6th sem\ERYX\eryx_en_windows_v3_0_0.ppn"]
#         )
        
#         paud = pyaudio.PyAudio()
#         audio_stream = paud.open(rate=porcupine.sample_rate, 
#                                  channels=1, 
#                                  format=pyaudio.paInt16, 
#                                  input=True, 
#                                  frames_per_buffer=porcupine.frame_length)
        
#         # Loop for streaming
#         while True:
#             keyword = audio_stream.read(porcupine.frame_length)
#             keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)

#             # Processing keyword from mic
#             keyword_index = porcupine.process(keyword)

#             # Check if "hey eryx" is detected
#             if keyword_index >= 0:
#                 print("Hotword 'Eryx' detected!")

#                 # Perform the action (press Shift + E)
#                 autogui.hotkey("shift", "e")
#                 time.sleep(2)
                
#     except Exception as e:
#         print(f"Error: {e}")
#     finally:
#         if porcupine is not None:
#             porcupine.delete()
#         if audio_stream is not None:
#             audio_stream.close()
#         if paud is not None:
#             paud.terminate()

# hotword()
import struct
import time
import pvporcupine
import pyaudio
import pyautogui as autogui
import threading
import traceback

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
                sensitivities=[0.95]  # Higher sensitivity
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
                time.sleep(0.1)  # Keeps the script running while reducing CPU usage

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

                # Debugging: Print active window
                active_window = autogui.getActiveWindow()
                print(f"Active window: {active_window}")

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

# Run the hotword detector in a separate thread
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
