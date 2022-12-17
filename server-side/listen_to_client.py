"""wait for client response
"""

import socket
import shutil
import json
import tqdm
import sys
import os

__home__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(__home__))
__home__ += "/"

from mytoolkit.txttag import TextTag as tag

config_file = open(f'{__home__}config.json', 'r')
configuration = json.load(config_file)

SERVER_HOST = configuration['serverIP']
SERVER_PORT = configuration['vanilla port']

config_file.close()

BUFFER_SIZE = 1024 * 4
SEPARATOR = "<SEPARATOR>"

socket_ref = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP)
socket_ref.bind((SERVER_HOST, SERVER_PORT))

socket_ref.listen(5)
print(f"{tag.info.b()}[*]{tag.info} Listening as {tag.id}{SERVER_HOST}{tag.white}:{tag.id}{SERVER_PORT}{tag.close}")

client_socket, address = socket_ref.accept()
print(f"{tag.info.b()}[+] {tag.id}{address}{tag.info} is connected.{tag.close}")

received = client_socket.recv(BUFFER_SIZE).decode()
filename, filesize = received.split(SEPARATOR)
filename = os.path.basename(filename)
filesize = int(filesize)

progress = tqdm.tqdm(
    range(filesize),
    f"Receiving {tag.id}{filename}{tag.close}",
    unit="B", unit_scale=True, unit_divisor=1024
    )

with open(f"{__home__}inbound/{filename}", "wb") as file_b:
    while True:
        bytes_read = client_socket.recv(BUFFER_SIZE)

        if not bytes_read: # Received empty Data
            break # Proceed to connection closure

        file_b.write(bytes_read)
        progress.update(len(bytes_read))

    file_b.flush() # Prompt I/O Buffer to write immediately

shutil.unpack_archive(f"{__home__}inbound/{filename}", f"{__home__}inbound/{'.'.join(address)}", 'zip')

client_socket.close()
socket_ref.close()
