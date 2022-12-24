"""invasively contact server
"""

import socket
import shutil
import tqdm
import json
import sys
import os

__home__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(__home__))

from mytoolkit.core.keymaker import generateAtDir as make_key_at
from mytoolkit.txttag import TextTag as tag
from mytoolkit.core.brain import fileThinker as thinker

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 1024 * 4

def check_keychain() -> None:
    """
    """
    if not os.path.isfile(f'{__home__}/metadata/privkey.pem'):
        try:
            make_key_at(f'{__home__}/metadata/', asym=True)
        
        except Exception as e:
            raise e

    if not os.path.isfile(f'{__home__}/metadata/key.key'):
        try:
            make_key_at(f'{__home__}/metadata/', asym=False)
        
        except Exception as e:
            raise e


def fetch_config(config_filename:str=f'{__home__}/metadata/config.json') -> dict:
    """
    Loads .json configurations onto a dictionary and returns it
    """
    config_file = open(config_filename)
    configuration = json.load(config_file)
    config_file.close()

    return configuration

def pack_package() -> str:
    """
    Zips and encrypts file based on algorithm contract.json
    """
    # Zip the container directory and store it in the parent directory
    compr_file = shutil.make_archive(f"{__home__}/outbound/container", 'zip', f'{__home__}/outbound/container')
    files_to_kill = os.listdir(f'{__home__}/outbound/container')

    for file in files_to_kill:
        os.remove(f'{__home__}/outbound/container/{file}')

    # Load in algorithm contract to specify operations
    alg_contract_file = open(f'{__home__}/outbound/algorithm contract.json')
    alg_contract:dict[str, str] = json.load(alg_contract_file)

    # Prepare processed file name
    encr_file = compr_file + '.encrypted'

    # Using contract process file; File is taken from metadata directory
    # Output is written into encr_file, Input from compr_file
    myThinker = thinker(sourceFile = compr_file, targetFile = encr_file, keyAddress=f'{__home__}/metadata/')
    myThinker.think(contract=alg_contract)
    myThinker.close()

    # Delete original unprocessed file
    os.remove(compr_file)

    # Return encrypted file address
    return encr_file

def pack_and_ship(host:str, port:str) -> None:
    """
    """
    try:
        # Pack and get package address (encrypted compressed file)
        package = pack_package()
        filesize = os.path.getsize(package)

        try:
            # Initiate socket
            socket_ref = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP)
            print(f"{tag.info.b()}[*]{tag.info} Connecting to {tag.id}{host}{tag.white}:{tag.id}{port}{tag.close}")
            
            # Establish connection to server
            socket_ref.connect((host, port))
            print(f"{tag.info.b()}[+]{tag.info} Connected.{tag.close}")

            # Send initial 'heads up' message
            socket_ref.send(f"{package}{SEPARATOR}{filesize}".encode())
            progress = tqdm.tqdm(
                range(filesize),
                f"Sending {tag.id}{package}{tag.close}",
                unit="B", unit_scale=True, unit_divisor=1024)

            # Open package and transmit data with BUFFER_SIZE as packet size
            with open(package, "rb") as file_b:
                while True:
                    bytes_read = file_b.read(BUFFER_SIZE)

                    if not bytes_read: # Sending empty (close connection)
                        break # Proceed to connection closure

                    socket_ref.sendall(bytes_read)
                    progress.update(len(bytes_read))
                file_b.flush()

            # Terminate transmission connection
            
            socket_ref.close()
            print(f"\n\r{tag.info.b()}[+]{tag.info} Connection to {tag.info.b()}{host}{tag.white}:{tag.info.b()}{port}{tag.info} closed.{tag.close}")
            

        except socket.timeout:
            print(f"\n\r{tag.error.b()}[-]{tag.error} Connection failed. Server connection timeout.{tag.close}")
        
        except socket.error as e:
            print(f"\n\r{tag.error.b()}[-]{tag.error} Connection failed. Server connection denied:\n\r{tag.close}{e}")
        
        except Exception as e:
            print(f"\n\r{tag.error.b()}[-]{tag.error} Encountered runtime error:\n\r{tag.close}{e}")

        finally:
            os.remove(package)
        
    except Exception as e:
        print(f'\r\n{tag.error.b()}ERROR:{tag.error} package failure: {tag.close}\n\r{e}')
        exit(1)

if __name__ == "__main__":
    # get server configurations
    check_keychain()

    configuration = fetch_config()

    # Process and send container to server wrt config file
    pack_and_ship(
            configuration["serverIP"],
            configuration["vanilla port"]
    )
