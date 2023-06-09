import socket
import os

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '192.168.136.228'
port = 12002
serversocket.bind((host, port))
print(host,port)
serversocket.listen()

while True:
    clientsocket, addr = serversocket.accept()

    print("Connected to %s" % str(addr))

    # know the command entered by the user
    command = clientsocket.recv(1024).decode()

    if command == "get":
        # receive file name from client
        filename = clientsocket.recv(1024).decode()

        # send file size to client
        filesize = os.path.getsize(filename)
        clientsocket.send(str(filesize).encode())

        # send file data to client
        with open(filename, 'rb') as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                clientsocket.send(data)
        print("sent bro!!!")

    elif command == "post":
        # receive file name from client
        filename = clientsocket.recv(1024).decode()

        # receive file size from client
        #filesize = int(clientsocket.recv(1024).decode())

        # receive file data from client
        with open(filename, 'wb') as f:
            while 1:
                data = clientsocket.recv(1024)
                if not data:
                    break
                f.write(data)
                #filesize -= len(data)
        print("received bro!!!!")
    else:
        print("Unknown command")

    clientsocket.close()
