import socket
from cryptography.fernet import Fernet

def generate_key() -> bytes:
    key = Fernet.generate_key()
    return key

def establish_connection(host, port, key):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
   
    conn, addr = server_socket.accept()   
    conn.sendall(key)
    conn.close()


key = generate_key()
establish_connection("127.0.0.1", 8443, key)
