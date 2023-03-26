import socket
import tqdm
import os
import sys

HOST='0.0.0.0'
PORT=8080
BUFFER_SIZE=4096

serversocket=socket.socket()
serversocket.bind((HOST,PORT))
print("Server listening..")
serversocket.listen()

clientsocket,address=serversocket.accept()
print(f"{address} connected..")


msg=clientsocket.recv(BUFFER_SIZE).decode('utf-8')      # know whether client sends or receives a file
if msg=="post":     # client wants to upload a file to the server
    filename=clientsocket.recv(BUFFER_SIZE).decode('utf-8')
    filesize=clientsocket.recv(BUFFER_SIZE).decode('utf-8')    
    filename=os.path.basename(filename)
    filesize=int(filesize)
    progress=tqdm.tqdm(range(filesize), f"receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open (filename,"wb") as f:     # open a file of the given name and write the received data into it (creation)
        while 1:
            bytes_read=clientsocket.recv(BUFFER_SIZE)
            if not bytes_read:
                break
            f.write(bytes_read)
            progress.update(len(bytes_read))

elif msg=="get":       # client wants a file from the server
    filename=clientsocket.recv(BUFFER_SIZE).decode('utf-8')     # get the desired filename
    try:
        filesize=int(os.path.getsize(filename))
    except:
        filesize=0
    if filesize==0:     # file not present in the server
        clientsocket.send(f"{filesize}".encode('utf-8'))
    else:       # file present in the server 
        clientsocket.send(f"{filesize}".encode('utf-8'))
        progress=tqdm.tqdm(range(filesize), f"sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename,"rb") as f:      # open fil ein read mode and send data chunks to the client
            while 1:
                bytes_read=f.read(BUFFER_SIZE)
                if not bytes_read:
                    break
                clientsocket.sendall(bytes_read)
                progress.update(len(bytes_read))





