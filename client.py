import socket
import tqdm
import os
import sys

BUFFER_SIZE=4096
HOST='127.0.0.1'
PORT=8080

clientsocket=socket.socket()
clientsocket.connect((HOST,PORT))
print("Connected to server..")
msg=input("Type 'get' to download files and 'post' to upload files..")
clientsocket.send(msg.encode('utf-8'))

if msg=="post":         # send file to server
    filename=input("File to upload: ")
    filesize=os.path.getsize(filename)
    clientsocket.send(f"{filename}".encode('utf-8'))    
    clientsocket.send(f"{filesize}".encode('utf-8'))
    progress=tqdm.tqdm(range(filesize), f"sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename,"rb") as f:      # read data chunks from the file and send them to server
        while 1:
            bytes_read=f.read(BUFFER_SIZE)
            if not bytes_read:
                break
            clientsocket.sendall(bytes_read)
            progress.update(len(bytes_read))

elif msg=="get":    # to get a file from the server
    filename=input("File to receive: ")    
    clientsocket.send(f"{filename}".encode('utf-8'))         # give the filename to server
    filesize=int(clientsocket.recv(BUFFER_SIZE).decode('utf-8'))    # receive the filesize of the file present in the server
    if filesize==0:     # file not present in the server
        print("File not present..")
    else:       # file present in the server
        print("File present and retrieving..")
        progress=tqdm.tqdm(range(filesize), f"receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open (filename,"wb") as f:     # create a file and write the data received from the server.
            while 1:
                bytes_read=clientsocket.recv(BUFFER_SIZE)
                if not bytes_read:
                    break
                f.write(bytes_read)
                progress.update(len(bytes_read))

else:
    print("Invalid command..")
            

