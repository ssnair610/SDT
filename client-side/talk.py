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

from mytoolkit.txttag import TextTag as tag
from mytoolkit.core.brain import fileThinker as thinker

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 1024 * 4

def fetch_config(config_filename:str=f'{__home__}/metadata/config.json') -> dict:
    """
    """
    config_file = open(config_filename)
    configuration = json.load(config_file)
    config_file.close()

    return configuration

def pack_package() -> str:
    """
    """
    compr_file = shutil.make_archive(f"{__home__}/outbound/container", 'zip', f'{__home__}/outbound/container')
    
    alg_contract_file = open(f'{__home__}/outbound/algorithm contract.json')
    alg_contract = json.load(alg_contract_file)

    encr_file = compr_file + '.encrypted'

    myThinker = thinker(sourceFile = compr_file, targetFile = encr_file, keyAddress=f'{__home__}/metadata/')
    myThinker.enforce(contract=alg_contract)
    myThinker.close()

    os.remove(compr_file)

    return encr_file

def pack_and_ship(host:str, port:str) -> None:
    """
    """
    try:
        package = pack_package()
        filesize = os.path.getsize(package)

        try:
            socket_ref = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP)
            print(f"{tag.info.b()}[*]{tag.info} Connecting to {tag.id}{host}{tag.white}:{tag.id}{port}{tag.close}")
            
            socket_ref.connect((host, port))
            print(f"{tag.info.b()}[+]{tag.info} Connected.{tag.close}")

            socket_ref.send(f"{package}{SEPARATOR}{filesize}".encode())
            progress = tqdm.tqdm(
                range(filesize),
                f"Sending {tag.id}{package}{tag.close}",
                unit="B", unit_scale=True, unit_divisor=1024)

            with open(package, "rb") as file_b:
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
            print(f"\n\r{tag.error.b()}[-]{tag.error} Connection failed. Server connection denied:\n\r{tag.close}{e}")
        
        except Exception as e:
            print(f"\n\r{tag.error.b()}[-]{tag.error} Encountered runtime error:\n\r{tag.close}{e}")
        
        finally:
            os.remove(package)
    
    except Exception as e:
        print(f'\r\n{tag.error.b()}ERROR:{tag.error} package failure: {tag.close}\n\r{e}')
        exit(1)

if __name__ == "__main__":
    configuration = fetch_config()
    
    pack_and_ship(
            configuration["serverIP"], 
            configuration["vanilla port"]
    )