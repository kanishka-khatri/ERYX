import os
import eel

# Initialize Eel with the frontend folder
eel.init("frontend")
os.system(r'"C:\\Program Files (x86)\\Microsoft\\Edge\Application\\msedge.exe" --app="http://localhost:5500/index.html"')

# Start the frontend directly as an app
eel.start('index.html', mode='edge', host='localhost', port=5500)
