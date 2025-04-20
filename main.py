import os
import eel

from backend.features import *
from backend.command import *

def start():
        # Initialize Eel with the frontend folder
    eel.init("frontend")

    playAssistantSound()
    # greetMe()

    
    os.system(r'"C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"" --app="http://localhost:5500/index.html"')
    

    # Start the frontend directly as an app
    eel.start('index.html', mode='edge', host='localhost', port=5500)