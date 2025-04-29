# import threading
# from backend.features import * 
# # To run ERYX
# def starteryx():
#         # Code for process 1
#         print("Process 1 is running.")
#         from main import start
#         start()
        

# # To run hotword
# def listenHotword():
#         # Code for process 2
#         print("Process 2 is running.")
#         from backend.features import hotword
#         hotword()


#     # Start both processes
# if __name__ == '__main__':
#     p1 = threading.Thread(target=starteryx, daemon=True)
#     p2 = threading.Thread(target=listenHotword, daemon=True)

#     p1.start()
#     p2.start()

#     p1.join()
#     p2.join()
#     print("System stop")
import threading
from backend.features import * 
from backend.db import authenticate_user

def login():
    print("=== LOGIN REQUIRED ===")
    username = input("Username: ")
    password = input("Password: ")
    if authenticate_user(username, password):
        print("Login successful!")
        return True
    else:
        print("Authentication failed.")
        return False

# To run ERYX
def starteryx():
    print("Process 1 is running.")
    from main import start
    start()

# To run hotword
def listenHotword():
    print("Process 2 is running.")
    from backend.features import hotword
    hotword()

# Start both processes
if __name__ == '__main__':
    if login():
        p1 = threading.Thread(target=starteryx, daemon=True)
        p2 = threading.Thread(target=listenHotword, daemon=True)

        p1.start()
        p2.start()

        p1.join()
        p2.join()
        print("System stop")
    else:
        print("Access denied.")