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


msg=clientsocket.recv(BUFFER_SIZE).decode('utf-8')
if msg=="post":
    filename=clientsocket.recv(BUFFER_SIZE).decode('utf-8')
    filesize=clientsocket.recv(BUFFER_SIZE).decode('utf-8')     # receive file from the client.
    filename=os.path.basename(filename)
    filesize=int(filesize)
    progress=tqdm.tqdm(range(filesize), f"receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open (filename,"wb") as f:
        while 1:
            bytes_read=clientsocket.recv(BUFFER_SIZE)
            if not bytes_read:
                break
            f.write(bytes_read)
            progress.update(len(bytes_read))
    sys.exit()
elif msg=="get":
    print("No getting bro..")

