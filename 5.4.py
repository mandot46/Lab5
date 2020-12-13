import socket
import tqdm
import os
import json
import sys

s = socket.socket()
print(f"[+] socket succesffuly created")

host = "192.168.0.135" 
port = 8888

s.bind((host,port))
print(f"[+] socket binded to " + str(port))

BUFFER_SIZE = 4096

SEPARATOR = "<SEPARATOR>"

s.listen(5)
print(f"[+] Socket is listening ")

client_socket, address = s.accept()

print(f"[+] {address} is connected.")

received = client_socket.recv(BUFFER_SIZE).decode()
filename, filesize = received.split(SEPARATOR)

filename = os.path.basename(filename)

filesize = int(filesize)

progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "wb") as f:
    for _ in progress:
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:    
            break
        f.write(bytes_read)
        progress.update(len(bytes_read))
client_socket.close()
s.close()
