import sys
import os

__home__ = os.path.dirname(__file__)
sys.path.append(os.path.dirname(os.path.dirname(__home__)))
__home__ += "/"

from mytoolkit.txttag import TextTag as tag
import core.custom_encrypt as custom_enc

class des:
    @staticmethod
    def encryption(dataFile, key):
        try:
            des_instance = custom_enc.des(key[:8])

            print(f"{tag.info.b()}[*]{tag.info} Encrypting: {tag.id}{dataFile.name[:-15]}...{tag.close}")

            try:
                dataFile.seek(0)
                ciphertext = des_instance.encrypt(dataFile.read(), padmode=custom_enc.PAD_PKCS5)

                return ciphertext
            
            except Exception as e:
                print(f"{tag.error.b()}[-] ERROR:{tag.error} Encryption failed.{tag.close}\r\n{e}")
                raise e
            
        except Exception as e:
            print(f"{tag.error.b()}[-] ERROR:{tag.error} DES instance failed to initialize.{tag.close}\r\n{e}")
            raise e
        
    @staticmethod
    def encryptionstr(data:str, key):
        des_instance = custom_enc.des(key[:8])

        print(f"{tag.info.b()}[*]{tag.info} Encrypting: {tag.id}{data[:-15]}...{tag.close}")

        try:
            ciphertext = des_instance.encrypt(data.encode(), padmode=custom_enc.PAD_PKCS5)
            # print(f"{tag.info.b()}[+] Encryption: {tag.info}{ciphertext}{tag.close}")
            
            return ciphertext
        
        except Exception as e:
            print(f"{tag.error.b()}[-] ERROR:{tag.error} Encryption failed.{tag.close}\r\n{e}")
            raise e
    
    @staticmethod
    def decryption(dataFile, key):
        try:
            des_instance = custom_enc.des(key[:8])
            
            print(f"{tag.info.b()}[*]{tag.info} Decrypting: {tag.id}{dataFile.name[:-15]}...{tag.close}")
        
            try:
                dataFile.seek(0)
                # input('wait')

                plaintext = des_instance.decrypt(dataFile.read(), padmode=custom_enc.PAD_PKCS5)
                # ciphertext = des_instance.encrypt(dataFile.read(), padmode=custom_enc.PAD_PKCS5)
                # print(f"{tag.info.b()}[+] Encryption: {tag.info}{ciphertext}{tag.close}")
                
                print(f"{tag.info.b()}[*]{tag.info} Decrypted {tag.id}{dataFile.name}{tag.close}")
                return plaintext
            
            except Exception as e:
                print(f"{tag.error.b()}[-] ERROR:{tag.error} Encryption failed.{tag.close}\r\n{e}")
                raise e
        
        except Exception as e:
            print(f"{tag.error.b()}[-] ERROR:{tag.error} DES instance failed to initialize.{tag.close}\r\n{e}")
            raise e

    @staticmethod
    def decryptionstr(data, key):
        try:
            des_instance = custom_enc.des(key[:8])
            # data_b = data.encode().hex()
            # print(f"{tag.info.b()}[*]{tag.info} Decrypting: {tag.id}{data_b}{tag.close}")
            # print(f"{tag.info.b()}[@]{tag.info} Key {tag.id}{key.export_key(format='DER')[:8]}{tag.close}")

            try:

                plaintext = des_instance.decrypt(data, padmode=custom_enc.PAD_PKCS5)
                # print(f"{tag.info.b()}[@]{tag.info} plaintext: {tag.id}{plaintext}{tag.close}")
                # ciphertext = des_instance.encrypt(dataFile.read(), padmode=custom_enc.PAD_PKCS5)
                # print(f"{tag.info.b()}[+] Encryption: {tag.info}{ciphertext}{tag.close}")
                
                # print(f"{tag.info.b()}[*]{tag.info} Decrypted {tag.id}{data}{tag.close}")
                return plaintext
            
            except Exception as e:
                print(f"{tag.error.b()}[-] ERROR:{tag.error} Encryption failed.{tag.close}\r\n{e}")
                raise e
        
        except Exception as e:
            print(f"{tag.error.b()}[-] ERROR:{tag.error} DES instance failed to initialize.{tag.close}\r\n{e}")
            raise e
        
