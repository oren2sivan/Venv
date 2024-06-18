import socket

def Client_Establish():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "127.0.0.1"  
    server_port = 8002  
    client.connect((server_ip, server_port))
    print("Connected to the server")

    command_type=input("Enter the command type: upload/download   ")
    file_name= input("Enter the file name:  ")

    client.send(command_type.encode("utf-8")[:1024]) # sending the recommended command
    client.send(file_name.encode("utf-8")[:1024]) # sending the file name 

    if command_type=="upload":
        upload_from_client(file_name,client)

    elif command_type=="download":
        download_from_server(file_name,client)

def upload_from_client(file_name,client):
    with open(file_name,'rb') as file:
            data=file.read(1024)
            while data:
                client.send(data) 
                data=file.read(1024)
    print("File uploaded successfully")

def download_from_server(file_name,client):
    path="C:\\Users\\Oren\\Downloads\\"+file_name
    with open(path, 'wb') as file:
        data=client.recv(1024)
        while data:
            file.write(data)
            data=client.recv(1024)
    print("File downloaded successfully")

Client_Establish()