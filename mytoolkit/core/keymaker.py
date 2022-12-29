from Crypto.PublicKey import ECC
import sys
import os

__home__ = os.path.dirname(__file__)
sys.path.append(os.path.dirname(__home__))

from txttag import TextTag as tag

def generateAtDir(directory:str, asym:bool=False, curve='P-256') -> str:

    if asym:
        print(f"{tag.info.b()}[*]{tag.info} Generating ECC key for curve {tag.id}{curve}{tag.close}")
         
        try:
            key = ECC.generate(curve=curve) 
            print(f"{tag.info.b()}[+]{tag.info} Key generated.")
            
            with open(f"{directory}privkey.pem", "wb") as private_key_file:
                print(f"{tag.info.b()}[*]{tag.info} Writing key data to parent directory {tag.id}{directory}{tag.close}")
                private_key_file.write(str(key.export_key(format='PEM', use_pkcs8=True)).encode())
                private_key_file.close()
                print(f"{tag.info.b()}[+]{tag.info} Key stored successfully.")
        
            return f"{directory}privkey.pem"

        except Exception as e:
            print(f"{tag.error.b()}[-] ERROR:{tag.error} Key generation failed.{tag.close}\r\n")
            raise e
    
    else:
        print(f"{tag.info.b()}[*]{tag.info} Generating private key{tag.close}")
        
        try:
            print(f"{tag.info.b()}[+]{tag.info} Key generated.")
            
            with open(f"{directory}key.key", "wb") as private_key_file:
                print(f"{tag.info.b()}[*]{tag.info} Writing key data to parent directory {tag.id}{directory}{tag.close}")
                private_key_file.write(os.urandom(32))
                private_key_file.close()
                print(f"{tag.info.b()}[+]{tag.info} Key stored successfully.")
        
            return f"{directory}key.key"

        except Exception as e:
            print(f"{tag.error.b()}[-] ERROR:{tag.error} Key generation failed.{tag.close}\r\n")
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
