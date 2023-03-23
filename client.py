import socket
import tqdm
import os

BUFFER_SIZE=4096
HOST='127.0.0.1'
PORT=8080
SEPARATOR="<SEPARATOR>"

print("get <filename> to receive files from the server..")
clientsocket=socket.socket()
clientsocket.connect((HOST,PORT))
print("Connected to server..")

while 1:    
    filename=input("File path: ")
    try:
        filesize=os.path.getsize(filename)
    except FileNotFoundError:
        print("File not found: ")
        continue
    break

clientsocket.send(f"{filename}".encode('utf-8'))
clientsocket.send(f"{filesize}".encode('utf-8'))
progress=tqdm.tqdm(range(filesize), f"sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename,"rb") as f:
    while 1:
        bytes_read=f.read(BUFFER_SIZE)
        if not bytes_read:
            break
        clientsocket.sendall(bytes_read)
        progress.update(len(bytes_read))
