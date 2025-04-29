# # import struct
# # import time
# # import pvporcupine
# # import pyaudio
# # import pyautogui as autogui
# # import threading
# # import traceback

# # class HotwordDetector:
# #     def __init__(self):
# #         self.porcupine = None
# #         self.paud = None
# #         self.audio_stream = None
# #         self.running = True  # Control loop execution

# #     def start(self):
# #         try:
# #             print("Initializing Hotword Detector...")
# #             access_key = "l1dEfraxGosyk1c6rCVuKJIKPbteE/xApZyUpeme0cVAeajR8WnsZA=="  # Replace with your actual access key

# #             # Load Porcupine wake word detection
# #             self.porcupine = pvporcupine.create(
# #                 access_key=access_key,
# #                 keyword_paths=[r"D:\Project-6th sem\ERYX\eryx_en_windows_v3_0_0.ppn"],
# #                 sensitivities=[0.95]  # Higher sensitivity
# #             )

# #             self.paud = pyaudio.PyAudio()
# #             self.audio_stream = self.paud.open(
# #                 rate=self.porcupine.sample_rate,
# #                 channels=1,
# #                 format=pyaudio.paInt16,
# #                 input=True,
# #                 frames_per_buffer=self.porcupine.frame_length,
# #                 stream_callback=self.callback
# #             )

# #             print("Listening for 'Eryx' hotword...")
# #             self.audio_stream.start_stream()

# #             while self.running:
# #                 time.sleep(0.1)  # Keeps the script running while reducing CPU usage

# #         except Exception as e:
# #             print(f"Error: {e}")
# #             with open("error_log.txt", "w") as f:
# #                 f.write(traceback.format_exc())  # Log errors

# #         finally:
# #             self.cleanup()

# #     def callback(self, in_data, frame_count, time_info, status):
# #         try:
# #             keyword = struct.unpack_from("h" * self.porcupine.frame_length, in_data)
# #             keyword_index = self.porcupine.process(keyword)

# #             if keyword_index >= 0:
# #                 print("Hotword 'Eryx' detected! Triggering shortcut...")

# #                 # Debugging: Print active window
# #                 active_window = autogui.getActiveWindow()
# #                 print(f"Active window: {active_window}")

# #                 # Trigger Ctrl + Shift + E
# #                 autogui.hotkey("ctrl", "shift", "e")

# #         except Exception as e:
# #             print(f"Callback Error: {e}")
# #             with open("error_log.txt", "a") as f:
# #                 f.write(traceback.format_exc())  # Log errors

# #         return (in_data, pyaudio.paContinue)

# #     def stop(self):
# #         self.running = False

# #     def cleanup(self):
# #         if self.porcupine:
# #             self.porcupine.delete()
# #         if self.audio_stream:
# #             self.audio_stream.stop_stream()
# #             self.audio_stream.close()
# #         if self.paud:
# #             self.paud.terminate()
# #         print("Stopped listening.")

# # # Run the hotword detector in a separate thread
# # try:
# #     detector = HotwordDetector()
# #     thread = threading.Thread(target=detector.start, daemon=True)
# #     thread.start()

# #     while True:
# #         command = input("Type 'exit' to stop: ").strip().lower()
# #         if command == "exit":
# #             detector.stop()
# #             break

# # except Exception as e:
# #     with open("error_log.txt", "w") as f:
# #         f.write(traceback.format_exc())  # Log startup errors

# # test_close.py
# import sys
# import os
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# from backend.features import opencommand
# from backend.features import closecommand
# opencommand("open youtube")
# closecommand("close youtube")
from backend.db import register_user

username = input("Set a username: ")
password = input("Set a password: ")

if register_user(username, password):
    print("User registered successfully!")
else:
    print("Username already exists.")