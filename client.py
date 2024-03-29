import socket
import os
import tqdm
import time

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '10.30.205.70'
port = 12003
clientsocket.connect((host, port))

command = input("Enter command get/post: ")
clientsocket.send(command.encode())

if command == "get":
    # get file name from user
    filename = input("Enter file name: ")
    clientsocket.send(filename.encode())

    # receive file size from server
    filesize = int(clientsocket.recv(1024).decode())
    print(f"File size: {filesize} bytes")

    progress=tqdm.tqdm(range(filesize), f"sending {filename}", unit='B', unit_scale=True, unit_divisor=1024)
    # receive file data from server
    with open(filename, 'wb') as f:
        while filesize > 0:
            data = clientsocket.recv(1024)
            f.write(data)
            filesize -= len(data)
            progress.update(len(data))

    print(f"Received file: {filename}")

elif command == "post":
    # get file name from user
    filename = input("Enter file name: ")
    #filename=os.path.basename(filename)
    clientsocket.send(f"{filename}".strip().encode('utf-8'))
    # send file size to server
    filesize = int(os.path.getsize(filename))
    #clientsocket.send(str(filesize).strip().encode())
    time.sleep(2)

    progress=tqdm.tqdm(range(filesize), f"sending {filename}", unit='B', unit_scale=True, unit_divisor=1024)
    # send file data to server
    with open(filename, 'rb') as f:
        while True:
            data = f.read(1024)
            if not data:
                break
            clientsocket.sendall(data)
            progress.update(len(data))
    clientsocket.close()

    print(f"Sent file: {filename}")
else:
    print("Unknown command")

clientsocket.close()
