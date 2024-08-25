import socket
import tkinter as tk
import hashmd5 

# connect with: username- oren, password- 521242

sign_in_respond=None
execute_result=None

def connect(ip,port):
    
    socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket1.connect((ip, port))
    print(f"connect to server:{ip}")
    return socket1

socket1=connect('127.0.0.1',8082)

def sign_in(username,password, socket=socket1):
    hash_passwd=hashmd5.hash(password)
    socket.sendall(username.encode())
    socket.sendall(hash_passwd.encode())
    response=socket.recv(1024).decode()
    if response=='1':
        return True
    else:
        print("error has been found. cannot connect")
        return False
    

def remote_execute(command, socket=socket1):
    global execute_result
    socket.sendall(command.encode())
    execute_result=socket.recv(1024).decode()
    return execute_result
    

def fetch_info_sign_in():
    username=username_box.get()
    password=password_box.get()
    return username, password


def sign_in_success():
    
    for widget in root.winfo_children():
        widget.destroy()
    new_label = tk.Label(root, text="enter name of command to be executed!", font="David")
    new_label.pack(pady=5)

    command_box = tk.Entry(root, width=30)
    command_box.pack(pady=5)

    def send_command():
        command = command_box.get()
        execute_result = remote_execute(command, socket1)
        print(execute_result)
        if execute_result!=None:
            result_label = tk.Label(root, text=execute_result, font="David")
            result_label.pack(pady=10)
    
    send_button=tk.Button(root, text="Send", width=10,command=send_command)
    send_button.pack(pady=5)
    


def handle_sign_in():
    global sign_in_respond
    attempts = 0
    max_attempts = 3
    
    while attempts <= max_attempts:
        username, password = fetch_info_sign_in()
        sign_in_respond = sign_in(username, password)
        if sign_in_respond:
            sign_in_success()
            return  
        else:
            attempts += 1
            result_label = tk.Label(root, text="Invalid username or password. try again", font="David")
            result_label.place(x=150, y=250)
            break

        



root = tk.Tk()

root.title("My Tkinter Window")

# Set the window size
root.geometry("700x600")  # Width x Height

welcome_label = tk.Label(root, text="Welcome!",font="David").place(x=200, y=50)
# Add a label widget
username_label = tk.Label(root, text="Username:",font="David").place(x=50, y=100)
username_box = tk.Entry(root, width=30)
username_box.place(x=150, y=100)

password_label = tk.Label(root, text="Password:",font="David").place(x=50, y=150)
password_box = tk.Entry(root, width=30)
password_box.place(x=150, y=150)


sign_in_button = tk.Button(root, text="Sign In", width=10,command=handle_sign_in).place(x=200, y=200)


# Run the application
root.mainloop()


