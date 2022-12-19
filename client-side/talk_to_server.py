"""invasively contact server
"""

import socket
import argparse
import shutil
import tqdm
import json
import sys
import os

__home__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(__home__))
__home__ += "/"

from mytoolkit.txttag import TextTag as tag

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 1024 * 4

def fetch_config(config_filename:str=f'{__home__}config.json') -> dict:
    config_file = open(config_filename)
    configuration = json.load(config_file)
    config_file.close()

    return configuration

def send_file(filename:str, host:str, port:str):
    """Sends a file given its name to a designated host IP and port address/number

    Args:
        filename (str): Name of the file (if possible with relative path)
        host (str): expectant reciever's IP address
        port (str): expactant port address for the reciever
    """
    zipped:bool = False

    if filename == '../':
        zipped = True
        filename = shutil.make_archive(f"{__home__}client{hash((host, port))}", 'zip', f'{__home__}outbound')
    else:
        filename = f"{__home__}outbound/{filename}"
    
    filesize = os.path.getsize(filename)
    print(f"{tag.id.b()}{filename}{tag.info} size: {tag.info.b()}{filesize}{tag.close}")

    try:
        socket_ref = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP)
        print(f"{tag.info.b()}[*]{tag.info} Connecting to {tag.id}{host}{tag.white}:{tag.id}{port}{tag.close}")
        
        socket_ref.connect((host, port))
        print(f"{tag.info.b()}[+]{tag.info} Connected.{tag.close}")

        socket_ref.send(f"{filename}{SEPARATOR}{filesize}".encode())
        progress = tqdm.tqdm(
            range(filesize),
            f"Sending {tag.id}{filename}{tag.close}",
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
        print(f"\n\r{tag.info.b()}[+]{tag.info} Connection to {tag.info.b()}{host}{tag.white}:{tag.info.b()}{port}{tag.info} closed.{tag.close}")

    except socket.timeout:
        print(f"\n\r{tag.error.b()}[-]{tag.error} Connection failed. Server connection timeout.{tag.close}")
    
    except socket.error as e:
        print(f"\n\r{tag.error.b()}[-]{tag.error} Connection failed. Server connection denied.\n\r{tag.close}{e}")
    
    except Exception as e:
        print(f"\n\r{tag.error.b()}[-]{tag.error} Encountered runtime error.\n\r{tag.close}{e}")
    
    finally:
        if zipped:
            os.remove(filename)

if __name__ == "__main__":
    # import argparse
    parser = argparse.ArgumentParser()

    configuration = fetch_config()

    parser.add_argument("file", help="File name to send", default='../')
    parser.add_argument("-host", help="The host/IP address of the receiver", default=configuration['serverIP'])
    parser.add_argument("-p", "--port", help=f"Port to use, default is {configuration['vanilla port']}", default=configuration['vanilla port'])

    args = parser.parse_args()

    filename = args.file
    host = args.host
    port = args.port

    send_file(filename, host, port)
