"""sender module
"""

import socket
import os
import argparse
import tqdm
import json

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 1024 * 4

def fetch_config(config_filename:str='config.json') -> dict:
    config_file = open(config_filename)
    configuration = json.load(config_file)
    config_file.close()

    return configuration

def send_file(filename, host, port):
    """Sends a file given its name to a designated host IP and port address/number

    Args:
        filename (str): Name of the file (if possible with relative path)
        host (str): expectant reciever's IP address
        port (str): expactant port address for the reciever
    """

    filename = "outbound/" + filename
    filesize = os.path.getsize(filename)
    print(f"{filename} size: {filesize}")

    socket_ref = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP)
    print(f"[+] Connecting to {host}:{port}")

    socket_ref.connect((host, port))
    print("[+] Connected.")

    socket_ref.send(f"{filename}{SEPARATOR}{filesize}".encode())
    progress = tqdm.tqdm(
        range(filesize),
        f"Sending {filename}",
        unit="B", unit_scale=True, unit_divisor=1024)

    with open(filename, "rb") as file_b:
        while True:
            bytes_read = file_b.read(BUFFER_SIZE)

            if not bytes_read: # Sending empty (close connection)
                break # Proceed to connection closure

            socket_ref.sendall(bytes_read)
            progress.update(len(bytes_read))
        file_b.flush()

    socket_ref.close()
    print(f"[+] Connection to {host}:{port} closed.")

if __name__ == "__main__":
    # import argparse
    parser = argparse.ArgumentParser()

    configuration = fetch_config()

    parser.add_argument("file", help="File name to send")
    parser.add_argument("-host", help="The host/IP address of the receiver", default=configuration['serverIP'])
    parser.add_argument("-p", "--port", help=f"Port to use, default is {configuration['vanilla port']}", default=configuration['vanilla port'])

    args = parser.parse_args()

    filename = args.file
    host = args.host
    port = args.port

    send_file(filename, host, port)
