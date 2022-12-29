from Crypto.PublicKey import ECC
import sys
import os
import logging

key_logger = logging.getLogger("Key maker logger")
key_logger.propagate = False
key_logger.setLevel(logging.INFO)
if not key_logger.handlers:
    fh = logging.FileHandler(filename='key_history.log')
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
    fh.setFormatter(formatter)
    key_logger.addHandler(fh)

__home__ = os.path.dirname(__file__)
sys.path.append(os.path.dirname(__home__))

from txttag import TextTag as tag

def generateAtDir(directory:str, asym:bool=False, curve='P-256') -> str:

    if asym:
        print(f"{tag.info.b()}[*]{tag.info} Generating ECC key for curve {tag.id}{curve}{tag.close}")
        key_logger.info("ECC key generation invoked.")
        
        try:
            key = ECC.generate(curve=curve)
            print(f"{tag.info.b()}[+]{tag.info} Key generated.")
            key_logger.info("Key generated.")
            
            with open(f"{directory}privkey.pem", "wb") as private_key_file:
                print(f"{tag.info.b()}[*]{tag.info} Writing key data to parent directory {tag.id}{directory}{tag.close}")
                key_logger.info("Key Data written on to parent directory.")
                private_key_file.write(str(key.export_key(format='PEM', use_pkcs8=True)).encode())
                private_key_file.close()
                print(f"{tag.info.b()}[+]{tag.info} Key stored successfully.")
                key_logger.info("Key stored successfully.")
        
            return f"{directory}privkey.pem"

        except Exception as e:
            print(f"{tag.error.b()}[-] ERROR:{tag.error} Key generation failed.{tag.close}\r\n")
            key_logger.error("Key generation failed.")
            raise e
    
    else:
        print(f"{tag.info.b()}[*]{tag.info} Generating private key{tag.close}")
        key_logger.info("Private key generation invoked.")
        try:
            print(f"{tag.info.b()}[+]{tag.info} Key generated.")
            key_logger.info("Key generated.")
            with open(f"{directory}key.key", "wb") as private_key_file:
                print(f"{tag.info.b()}[*]{tag.info} Writing key data to parent directory {tag.id}{directory}{tag.close}")
                key_logger.info("Writing key data onto parent directory.")
                private_key_file.write(os.urandom(32))
                private_key_file.close()
                print(f"{tag.info.b()}[+]{tag.info} Key stored successfully.")
                key_logger.info("Key stored successfully.")
        
            return f"{directory}key.key"

        except Exception as e:
            print(f"{tag.error.b()}[-] ERROR:{tag.error} Key generation failed.{tag.close}\r\n")
            key_logger.error("Key generation failed.")
            raise e
        

def getFromFile(filename:str):
    file_ext = os.path.splitext(filename)[1]

    if file_ext == '.pem':
        priv_key_file = open(filename, 'rb')
        priv_key = ECC.import_key(priv_key_file.read())
        priv_key_file.close()
        
        return priv_key
    
    elif file_ext == '.key':
        sym_key_file = open(filename, 'rb')
        sym_key = sym_key_file.read()
        sym_key_file.close()

        return sym_key
    
    else:
        print(f"{tag.error.b()}[-] ERROR:{tag.error} Key extension not recognized.\r\nGiven filename: {tag.id}{filename}{tag.close}\r\n")
        raise ValueError('key extension not supported')
