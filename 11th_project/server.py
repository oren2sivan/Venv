import socket
import dbhandle as db 
import subprocess as sp



def establish(ip,port):
    socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket1.bind((ip, port))  
    socket1.listen(1)
    print(f"server listening on ip: { ip}, and port: {port }")
    
    socket1,add=socket1.accept()
    print(f" connected to: {add}")
    return socket1


def authenticate(socket1):
    max_attempts = 4
    for attempt in range(max_attempts):
        username = socket1.recv(1024).decode()
        hash_passwd = socket1.recv(1024).decode()
        result = db.find_user(username, hash_passwd)
        if result:
            socket1.send("1".encode())
            return True
        else:

            socket1.send("0".encode())
            if attempt < max_attempts :
                print("Invalid credentials. try again")
            else:
                return False
    return False
    




def execute_command(socket1):
    command=socket1.recv(1024).decode()
    result = sp.run(command, shell=True, capture_output=True, text=True)
    output = result.stdout
    print(output)
    socket1.sendall(output.encode())

def run_server():

    socket1=establish("127.0.0.1", 8082)
    authenticate(socket1)
    execute_command(socket1)
    socket1.close()

if __name__=="__main__":
    run_server()