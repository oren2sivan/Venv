import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 55557))
s.listen(1)
Client_socket, address = s.accept()

print('client connected')
while(True):
    data = Client_socket.recv(1024).decode()
    if data=='stop':
        break
    print('client sent: '+ data)
    reply = input("answer: ")
    Client_socket.send(reply.encode())
Client_socket.close()
s.close()
