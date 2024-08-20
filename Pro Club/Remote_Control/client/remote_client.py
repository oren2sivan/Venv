import pyautogui
import time 
from pynput import keyboard, mouse
import socket
import threading
from PIL import Image, ImageTk
import io
import json
import tkinter as tk

#good 
def connect(host, port):
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s1.connect((host, port))
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2.connect((host, port+1))
    return s1,s2

#good 
def keyboard_activity(socket1):
    def on_press(key):
        try:
            data = {'keyboard': key.char}
        except AttributeError:
            data={'keyboard': key.name}
            print(data)
            
        data_json=json.dumps(data)
        socket1.sendall(data_json.encode())

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

#good
def mouse_location(socket):
    while True:
        x, y = pyautogui.position()
        data ={'mouse': 'position','position': (x, y)}
        data_json=json.dumps(data)
        socket.sendall(data_json.encode())

        time.sleep(0.2)

#good
def check_mouse_clicks(socket):
    def on_click(x, y, button, pressed):
        if pressed:
            
            data = {'mouse': str(button),'position':(x,y)}
            data_json=json.dumps(data)
            socket.sendall(data_json.encode())
            
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

#good
def display_image(socket2, label):
    while True:
        # Receive the length of the image data
        image_len = int.from_bytes(socket2.recv(4), byteorder='big')
        
        # Receive the image data
        img_data = b""
        while len(img_data) < image_len:
            packet = socket2.recv(4096)
            if not packet:
                break
            img_data += packet

        # Convert the data to an image
        try:
            image = Image.open(io.BytesIO(img_data))
            image = ImageTk.PhotoImage(image)

            # Update the label with the new image
            label.config(image=image)
            label.image = image  # Keep a reference to avoid garbage collection
        except Exception as e:
            print(f"Error: {e}")



            

       

# Start client and threads

#good
def run(ip,port):
    socket1,socket2 = connect(ip, port)
    root = tk.Tk()
    root.title("Screen Stream")

    label = tk.Label(root)
    label.pack()

    thread_list = [
        threading.Thread(target=display_image, args=(socket2, label)),
        threading.Thread(target=keyboard_activity, args=(socket1,)),
        threading.Thread(target=mouse_location, args=(socket1,)),
        threading.Thread(target=check_mouse_clicks, args=(socket1,))
    ]

    for thread in thread_list:
        thread.start()

    root.mainloop()  # Ensure the Tkinter window stays open

    for i in thread_list:
        i.join()

    socket1.close()
    socket2.close()

run('10.0.0.6',9095)


#last version