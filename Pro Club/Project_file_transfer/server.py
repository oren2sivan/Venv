import socket
import sqlite3

def initialize_db():
    conn = sqlite3.connect('files_DB.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS files (id INTEGER PRIMARY KEY AUTOINCREMENT,filename TEXT NOT NULL,filedata BLOB NOT NULL)''')
    conn.commit()
    return conn, cursor
# i have 3 variable in db:
#id- row number
#filename- name of file
#filedata- data of file





def Server_Establish():
    conn, cursor = initialize_db()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "127.0.0.1"  #ip of me beacause im binding with the same machine
    port = 8002
    server.bind((server_ip, port))


    server.listen(1)# האזנה לכל היותר למשתמש אחד
    print(f"Listening on {server_ip} : {port}")

    client_socket, client_address = server.accept()#accept returns a tuple of a new socket and adress(ip,port) of the client.
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
    #till now i established a connection

    # now lets start with the upload/download:
    command_type= client_socket.recv(1024).decode()#we get the command type from the client
    file_name=client_socket.recv(1024).decode()#we get the file name from the client

    #in case we want to upload a file:
    if command_type == "upload":
        Upload(client_socket, file_name,cursor,conn)
    elif command_type == "download":
        Download(client_socket, file_name, cursor, conn)
    client_socket.close()
    server.close()
    conn.close()



def IsIn(file_name, cursor):
    cursor.execute("SELECT 1 FROM files WHERE filename = ?", (file_name,))
    result = cursor.fetchone()
    return result!=None

def Upload(client_socket, file_name, cursor, conn):
    if IsIn(file_name, cursor)==True:
        print(f"File '{file_name}' already exists. choose a different name file ")
    else:    
        file_data = bytearray()
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            file_data.extend(data)
        cursor.execute("INSERT INTO files (filename, filedata) VALUES (?, ?)", (file_name, sqlite3.Binary(file_data)))
        conn.commit()

        print(f"'{file_name}' was received and uploaded successfully.")

def Download(client_socket, file_name, cursor, conn):
    cursor.execute("SELECT filedata FROM files WHERE filename = ?", (file_name, ))
    data=cursor.fetchone()[0]
    client_socket.sendall(data)
    print(f"'{file_name}' was sent to the client successfully.")
        



Server_Establish()
