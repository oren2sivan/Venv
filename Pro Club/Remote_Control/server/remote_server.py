import socket
import keyboard
import pyautogui
import time
from PIL import ImageGrab
import threading
import json
import io
class Server:
    #good
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s1.bind((self.host, self.port))
        self.s1.listen(1)

        self.s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s2.bind((self.host, self.port+1))
        self.s2.listen(1)


        print(f"Server listening on {self.host}:{self.port}")
        print(f"Server listening on {self.host}:{self.port+1}")

        self.socket1, self.addr = self.s1.accept()
        self.socket2, self.addr = self.s2.accept()

        print(f"Connection from {self.addr} on port {port}")
        print(f"Connection from {self.addr} on port {port+1}")

    #good
    def keyboard_press(self, key):
        print(f"Key pressed: {key}")
        special_keys = ['ctrl', 'alt', 'shift', 'enter', 'backspace', 'tab', 'esc','space']

        if key in special_keys:
            # Execute the special key press
            keyboard.press(key)
            keyboard.release(key)
        else:
            keyboard.write(key)
    #good
    def move_mouse_position(self, x, y):
        pyautogui.moveTo(x, y)

    #good
    def click_mouse_left(self):
        pyautogui.leftClick()

    #good
    def click_mouse_right(self):
        pyautogui.rightClick()


    #good 
    def capture_and_display_screen(self, fps=30):
        interval = 1.0 / fps
        while True:
            # Capture the screen using ImageGrab
            screenshot = ImageGrab.grab()

            # Save the screenshot to a BytesIO buffer as a PNG image
            img_buffer = io.BytesIO()
            screenshot.save(img_buffer, format='PNG')
            img_bytes = img_buffer.getvalue()
            img_buffer.close()

            # Get the length of the image bytes
            image_len = len(img_bytes)

            # Send the length as a 4-byte integer
            self.socket2.sendall(image_len.to_bytes(4, byteorder='big'))

            # Send the actual image data
            self.socket2.sendall(img_bytes)

            time.sleep(interval)

            
    #bad
    def handle_client_commands(self):
        while True:
            
            data = self.socket1.recv(1024).decode()
            
            if not data:
                break
            try:
                data_dict = json.loads(data)  
                if "keyboard" in data_dict:# כל שימוש במקלדת
                    key=data_dict["keyboard"]
                    if data_dict["keyboard"] == 'esc':
                        self.socket1.close()
                        self.socket2.close()
                    else:
                    

                        self.keyboard_press(key)
                elif "mouse" in data_dict:  # הזזת עכבר למקום הנדרש
                    if data_dict["mouse"] == 'Button.left':
                        self.click_mouse_left()
                    elif data_dict["mouse"] == 'Button.right':
                        self.click_mouse_right()
                    elif "position" in data_dict:
                        x = data_dict["position"][0]
                        y = data_dict["position"][1]
                        self.move_mouse_position(x, y)
            except json.JSONDecodeError:
                print("Invalid JSON data received.")
           
    #good 
    def run(self):
        capture_thread = threading.Thread(target=self.capture_and_display_screen)
        command_thread = threading.Thread(target=self.handle_client_commands)
        
        capture_thread.start()
        command_thread.start()

        capture_thread.join()
        command_thread.join()

        self.socket1.close()
        self.socket2.close()

ex = Server('10.0.0.53', 8011)
ex.run()

#last version