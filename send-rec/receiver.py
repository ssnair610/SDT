"""receiver module
"""

import socket
import os
import tqdm

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5001

BUFFER_SIZE = 1024 * 4
SEPARATOR = "<SEPARATOR>"

socket_ref = socket.socket(proto=0)
socket_ref.bind((SERVER_HOST, SERVER_PORT))

socket_ref.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

client_socket, address = socket_ref.accept()
print(f"[+] {address} is connected.")

received = client_socket.recv(BUFFER_SIZE).decode()
filename, filesize = received.split(SEPARATOR)
filename = os.path.basename(filename)
filesize = int(filesize)

progress = tqdm.tqdm(
    range(filesize),
    f"Receiving {filename}",
    unit="B", unit_scale=True, unit_divisor=1024
    )

with open(filename, "wb") as file_b:
    while True:
        bytes_read = client_socket.recv(BUFFER_SIZE)

        if not bytes_read: # Received empty Data
            break # Proceed to connection closure

        file_b.write(bytes_read)
        progress.update(len(bytes_read))

    file_b.flush() # Prompt I/O Buffer to write immediately

client_socket.close()
socket_ref.close()