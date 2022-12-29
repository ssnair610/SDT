import time
import sys
import os
import logging

__home__ = os.path.dirname(__file__)
sys.path.append(os.path.dirname(__home__))

from txttag import TextTag as tag
import core.custom_encrypt as custom_enc

_latest_op_time:float = 0.0

e_logger = logging.getLogger("Encryption function logger")
e_logger.propagate = False
e_logger.setLevel(logging.INFO)
if not e_logger.handlers:
    fh = logging.FileHandler(filename='e_history.log')
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
    fh.setFormatter(formatter)
    e_logger.addHandler(fh)

class des:
    @staticmethod
    def encryption(dataFile, key:bytes):
        global _latest_op_time
        _latest_op_time = 0.0

        try:
            des_instance = custom_enc.des(key[:8])

            print(f"{tag.info.b()}[*]{tag.info} DES::Encrypting: {tag.id}{dataFile.name}{tag.close}")
            e_logger.info("DES encryption invoked.")

            try:
                dataFile.seek(0)
                
                _latest_op_time = time.perf_counter()
                ciphertext = des_instance.encrypt(dataFile.read(), padmode=custom_enc.PAD_PKCS5)
                _latest_op_time = time.perf_counter() - _latest_op_time

                return ciphertext

            except Exception as e:
                print(f"{tag.error.b()}[-] ERROR:{tag.error} Encryption failed.{tag.close}/r/n{e}")
                e_logger.error("Encryption failed.")
                raise e

        except Exception as e:
            print(f"{tag.error.b()}[-] ERROR:{tag.error} DES instance failed to initialize.{tag.close}/r/n{e}")
            e_logger.error("DES failed to initialize.")
            raise e

    @staticmethod
    def encryptionb(data:bytes, key:bytes):
        global _latest_op_time
        _latest_op_time = 0.0
        des_instance = custom_enc.des(key[:8])

        print(f"{tag.info.b()}[*]{tag.info} DES::Encrypting: {tag.id}{data}{tag.close}")
        e_logger.info("DES encryption invoked.")
        try:
            _latest_op_time = time.perf_counter()
            ciphertext = des_instance.encrypt(data, padmode=custom_enc.PAD_PKCS5)
            _latest_op_time = time.perf_counter() - _latest_op_time
            # print(f"{tag.info.b()}[+] Encryption: {tag.info}{ciphertext}{tag.close}")

            return ciphertext

        except Exception as e:
            print(f"{tag.error.b()}[-] ERROR:{tag.error} Encryption failed.{tag.close}/r/n{e}")
            e_logger.error("Encryption failed.")
            raise e

    @staticmethod
    def encryptionstr(data:str, key:bytes):
        global _latest_op_time
        _latest_op_time = 0.0
        des_instance = custom_enc.des(key[:8])

        print(f"{tag.info.b()}[*]{tag.info} DES::Encrypting: {tag.id}{data}{tag.close}")
        e_logger.info("DES encryption invoked.")
        try:
            _latest_op_time = time.perf_counter()
            ciphertext = des_instance.encrypt(data.encode(), padmode=custom_enc.PAD_PKCS5)
            _latest_op_time = time.perf_counter() - _latest_op_time
            # print(f"{tag.info.b()}[+] Encryption: {tag.info}{ciphertext}{tag.close}")

            return ciphertext

        except Exception as e:
            print(f"{tag.error.b()}[-] ERROR:{tag.error} Encryption failed.{tag.close}/r/n{e}")
            e_logger.error("Encryption failed.")
            raise e

    @staticmethod
    def decryption(dataFile, key:bytes):
        global _latest_op_time
        _latest_op_time = 0.0
        try:
            des_instance = custom_enc.des(key[:8])

            print(f"{tag.info.b()}[*]{tag.info} DES::Decrypting: {tag.id}{dataFile.name}{tag.close}")
            e_logger.info("DES decryption invoked.")
            try:
                dataFile.seek(0)
                # input('wait')

                _latest_op_time = time.perf_counter()
                plaintext:bytes = des_instance.decrypt(dataFile.read(), padmode=custom_enc.PAD_PKCS5)
                _latest_op_time = time.perf_counter() - _latest_op_time

                print(f"{tag.info.b()}[*]{tag.info} DES::Decrypted {tag.id}{dataFile.name}{tag.close}")
                e_logger.info("DES Decryption terminated")
                return plaintext

            except Exception as e:
                print(f"{tag.error.b()}[-] ERROR:{tag.error} Decryption failed.{tag.close}/r/n{e}")
                e_logger.error("Decryption failed.")
                raise e

        except Exception as e:
            print(f"{tag.error.b()}[-] ERROR:{tag.error} DES instance failed to initialize.{tag.close}/r/n{e}")
            e_logger.error("DES instance failed to initialize.")
            raise e

    @staticmethod
    def decryptionb(data:bytes, key:bytes):
        global _latest_op_time
        _latest_op_time = 0.0
        try:
            des_instance = custom_enc.des(key[:8])
            print(f"{tag.info.b()}[*]{tag.info} DES::Decrypting: {tag.id}{data}{tag.close}")
            e_logger.info("DES decryption invoked.")
            try:

                _latest_op_time = time.perf_counter()
                plaintext = des_instance.decrypt(data, padmode=custom_enc.PAD_PKCS5)
                _latest_op_time = time.perf_counter() - _latest_op_time

                # print(f"{tag.info.b()}[*]{tag.info} Decrypted {tag.id}{data}{tag.close}")
                return plaintext

            except Exception as e:
                print(f"{tag.error.b()}[-] ERROR:{tag.error} Decryption failed.{tag.close}/r/n{e}")
                e_logger.error("Decryption failed.")
                raise e

        except Exception as e:
            print(f"{tag.error.b()}[-] ERROR:{tag.error} DES instance failed to initialize.{tag.close}/r/n{e}")
            e_logger.error("DES instance failed to initialize.")
            raise e

    @staticmethod
    def decryptionstr(data:str, key:bytes):
        global _latest_op_time
        _latest_op_time = 0.0
        try:
            des_instance = custom_enc.des(key[:8])
            # data_b = data.encode().hex()
            print(f"{tag.info.b()}[*]{tag.info} Decrypting: {tag.id}{data}{tag.close}")
            e_logger.info("DES decryption invoked.")    
            try:

                _latest_op_time = time.perf_counter()
                plaintext = des_instance.decrypt(data.encode(), padmode=custom_enc.PAD_PKCS5)
                _latest_op_time = time.perf_counter() - _latest_op_time

                return plaintext

            except Exception as e:
                print(f"{tag.error.b()}[-] ERROR:{tag.error} Decryption failed.{tag.close}/r/n{e}")
                e_logger.error("Decryption failed.")
                raise e

        except Exception as e:
            print(f"{tag.error.b()}[-] ERROR:{tag.error} DES instance failed to initialize.{tag.close}/r/n{e}")
            e_logger.error("DES instance failed to initialize.")
            raise e

class aes:
    @staticmethod
    def encryption(dataFile, key:bytes):
        global _latest_op_time
        _latest_op_time = 0.0
        try:
            aes_instance = custom_enc.AES(master_key=key[:32])

            print(f"{tag.info.b()}[*]{tag.info} AES::Encrypting: {tag.id}{dataFile.name}{tag.close}")
            e_logger.info("AES encryption invoked.")
            try:
                dataFile.seek(0)
                _latest_op_time = time.perf_counter()
                
                block = dataFile.read(16)
                ciphertext = b''

                while block:
                    if len(block) < 16:
                        block += b''.join([ b' ' ] * (16 - len(block)))

                    ciphertext += aes_instance.encrypt_block(block)
                    block = dataFile.read(16)

                _latest_op_time = time.perf_counter() - _latest_op_time

                return ciphertext

            except Exception as e:
                print(f"{tag.error.b()}[-] ERROR:{tag.error} Encryption failed.{tag.close}/r/n{e}")
                raise e

        except Exception as e:
            print(f"{tag.error.b()}[-] ERROR:{tag.error} AES instance failed to initialize.{tag.close}/r/n{e}")
            _latest_op_time = time.perf_counter()
            _latest_op_time = time.perf_counter() - _latest_op_time
            raise e

    @staticmethod
    def encryptionb(data:str, key:bytes):
        global _latest_op_time
        _latest_op_time = 0.0
        des_instance = custom_enc.des(key[:8])

        print(f"{tag.info.b()}[*]{tag.info} Encrypting: {tag.id}{data}{tag.close}")
        e_logger.info("AES encryption invoked.")
        try:
            _latest_op_time = time.perf_counter()
            ciphertext = des_instance.encrypt(data, padmode=custom_enc.PAD_PKCS5)
            _latest_op_time = time.perf_counter() - _latest_op_time
            # print(f"{tag.info.b()}[+] Encryption: {tag.info}{ciphertext}{tag.close}")

            return ciphertext

        except Exception as e:
            print(f"{tag.error.b()}[-] ERROR:{tag.error} Encryption failed.{tag.close}/r/n{e}")
            raise e
    @staticmethod
    def encryptionstr(data:str, key:bytes):
        global _latest_op_time
        _latest_op_time = 0.0
        des_instance = custom_enc.des(key[:8])

        print(f"{tag.info.b()}[*]{tag.info} Encrypting: {tag.id}{data}{tag.close}")
        e_logger.info("AES encryption invoked.")
        try:
            _latest_op_time = time.perf_counter()
            ciphertext = des_instance.encrypt(data.encode(), padmode=custom_enc.PAD_PKCS5)
            _latest_op_time = time.perf_counter() - _latest_op_time
            # print(f"{tag.info.b()}[+] Encryption: {tag.info}{ciphertext}{tag.close}")

            return ciphertext

        except Exception as e:
            print(f"{tag.error.b()}[-] ERROR:{tag.error} Encryption failed.{tag.close}/r/n{e}")
            raise e

    @staticmethod
    def decryption(dataFile, key:bytes):
        global _latest_op_time
        _latest_op_time = 0.0
        try:
            aes_instance = custom_enc.AES(key[:32])

            print(f"{tag.info.b()}[*]{tag.info} AES::Decrypting: {tag.id}{dataFile.name}{tag.close}")
            e_logger.info("AES decryption invoked.")
            try:
                dataFile.seek(0)
                # input('wait')

                _latest_op_time = time.perf_counter()
                
                plaintext = b''
                block = dataFile.read(16)

                while block:
                    if len(block) < 16:
                        block += b''.join([ b' ' ] * (16 - len(block)))

                    plaintext += aes_instance.decrypt_block(block)
                    block = dataFile.read(16)

                _latest_op_time = time.perf_counter() - _latest_op_time
                # ciphertext = des_instance.encrypt(dataFile.read(), padmode=custom_enc.PAD_PKCS5)
                # print(f"{tag.info.b()}[+] Encryption: {tag.info}{ciphertext}{tag.close}")

                print(f"{tag.info.b()}[*]{tag.info} Decrypted {tag.id}{dataFile.name}{tag.close}")
                return plaintext.rstrip()

            except Exception as e:
                print(f"{tag.error.b()}[-] ERROR:{tag.error} Decryption failed.{tag.close}/r/n{e}")
                raise e

        except Exception as e:
            print(f"{tag.error.b()}[-] ERROR:{tag.error} AES instance failed to initialize.{tag.close}/r/n{e}")
            raise e

    @staticmethod
    def decryptionb(data:bytes, key:bytes):
        global _latest_op_time
        _latest_op_time = 0.0
        try:
            des_instance = custom_enc.des(key[:8])
            # data_b = data.encode().hex()
            # print(f"{tag.info.b()}[*]{tag.info} Decrypting: {tag.id}{data_b}{tag.close}")
            # print(f"{tag.info.b()}[@]{tag.info} Key {tag.id}{key.export_key(format='DER')[:8]}{tag.close}")

            try:
                _latest_op_time = time.perf_counter()
                plaintext = des_instance.decrypt(data, padmode=custom_enc.PAD_PKCS5)
                _latest_op_time = time.perf_counter() - _latest_op_time
                # print(f"{tag.info.b()}[@]{tag.info} plaintext: {tag.id}{plaintext}{tag.close}")
                # ciphertext = des_instance.encrypt(dataFile.read(), padmode=custom_enc.PAD_PKCS5)
                # print(f"{tag.info.b()}[+] Encryption: {tag.info}{ciphertext}{tag.close}")

                # print(f"{tag.info.b()}[*]{tag.info} Decrypted {tag.id}{data}{tag.close}")
                return plaintext

            except Exception as e:
                print(f"{tag.error.b()}[-] ERROR:{tag.error} Decryption failed.{tag.close}/r/n{e}")
                raise e

        except Exception as e:
            print(f"{tag.error.b()}[-] ERROR:{tag.error} DES instance failed to initialize.{tag.close}/r/n{e}")
            raise e

    @staticmethod
    def decryptionstr(data:str, key:bytes):
        global _latest_op_time
        _latest_op_time = 0.0
        try:
            des_instance = custom_enc.des(key[:8])
            # data_b = data.encode().hex()
            # print(f"{tag.info.b()}[*]{tag.info} Decrypting: {tag.id}{data_b}{tag.close}")
            # print(f"{tag.info.b()}[@]{tag.info} Key {tag.id}{key.export_key(format='DER')[:8]}{tag.close}")

            try:

                _latest_op_time = time.perf_counter()
                plaintext = des_instance.decrypt(data.encode(), padmode=custom_enc.PAD_PKCS5)
                _latest_op_time = time.perf_counter() - _latest_op_time
                # print(f"{tag.info.b()}[@]{tag.info} plaintext: {tag.id}{plaintext}{tag.close}")
                # ciphertext = des_instance.encrypt(dataFile.read(), padmode=custom_enc.PAD_PKCS5)
                # print(f"{tag.info.b()}[+] Encryption: {tag.info}{ciphertext}{tag.close}")

                # print(f"{tag.info.b()}[*]{tag.info} Decrypted {tag.id}{data}{tag.close}")
                return plaintext

            except Exception as e:
                print(f"{tag.error.b()}[-] ERROR:{tag.error} Decryption failed.{tag.close}/r/n{e}")
                raise e

        except Exception as e:
            print(f"{tag.error.b()}[-] ERROR:{tag.error} DES instance failed to initialize.{tag.close}/r/n{e}")
            raise e

if __name__ == '__main__':
    import sys
    # from Crypto.Cipher
    sys.path.append(__home__)

    file = open('D:/Projects/Code Stuff/Final Year Project/SDT-pythonic/client-side/metadata/key.key', 'rb')
    key = file.read()[:32]
    file.close()

    dat_file = open("D:/Projects/Code Stuff/Final Year Project/SDT-pythonic/client-side/metadata/config.json", 'rb')

    dat_file.flush()
    _aes = aes()

    enc = dat_file

    print(enc)
    enc = _aes.encryption(enc, key)
    print(enc)

    with open('weird', 'wb') as encr:
        encr.write(enc)

    with open('weird', 'rb') as encr:
        enc = _aes.decryption(encr, key)
    # enc = _aes.encrypt_block(enc)
    # print(enc)
    # enc = _aes.decrypt_block(enc)
        print(enc)

    dat_file.close()