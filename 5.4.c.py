import socket
import tqdm
import os
import json
import sys


SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096

s = socket.socket()
host = "192.168.0.135"
port = 8888

print(f"[+] Connecting to {host}:{port}")
s.connect((host,port))
print("[+] COnnected")

filename = input("Enter file name")
print("Filename:", filename)
filesize = os.path.getsize(filename)

s.send(f"{filename}{SEPARATOR}{filesize}".encode())

progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "rb") as f:
        for _ in progress:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                break
            s.sendall(bytes_read)
            progress.update(len(bytes_read))
s.close()
