import time
import sys
import os
import base64 as b64
from RC6Encryption import RC6Encryption as rc6_class

__home__ = os.path.dirname(__file__)
sys.path.append(os.path.dirname(__home__))

from txttag import TextTag as tag
import core.custom_encrypt as custom_enc

_latest_op_time:float = 0.0

class des:
    @staticmethod
    def encryption(dataFile, key:bytes):
        global _latest_op_time
        _latest_op_time = 0.0

        try:
            des_instance = custom_enc.des(key[:8])

            print(f"{tag.info.b()}[*]{tag.info} DES::Encrypting: {tag.id}{dataFile.name}{tag.close}")

            try:
                dataFile.seek(0)
                
                _latest_op_time = time.perf_counter()
                ciphertext = des_instance.encrypt(dataFile.read(), padmode=custom_enc.PAD_PKCS5)
                _latest_op_time = time.perf_counter() - _latest_op_time

                return ciphertext

            except Exception as e:
                print(f"{tag.error.b()}[-] ERROR:{tag.error} Encryption failed.{tag.close}/r/n{e}")
                raise e

        except Exception as e:
            print(f"{tag.error.b()}[-] ERROR:{tag.error} DES instance failed to initialize.{tag.close}/r/n{e}")
            raise e

    @staticmethod
    def encryptionb(data:bytes, key:bytes):
        global _latest_op_time
        _latest_op_time = 0.0
        des_instance = custom_enc.des(key[:8])

        print(f"{tag.info.b()}[*]{tag.info} DES::Encrypting: {tag.id}{data}{tag.close}")

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

        print(f"{tag.info.b()}[*]{tag.info} DES::Encrypting: {tag.id}{data}{tag.close}")

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
            dataFile.seek(0)
            des_instance = custom_enc.des(key[:8])

            print(f"{tag.info.b()}[*]{tag.info} DES::Decrypting: {tag.id}{dataFile.name}{tag.close}")

            try:
                dataFile.seek(0)
                # input('wait')

                _latest_op_time = time.perf_counter()
                plaintext:bytes = des_instance.decrypt(dataFile.read(), padmode=custom_enc.PAD_PKCS5)
                _latest_op_time = time.perf_counter() - _latest_op_time

                print(f"{tag.info.b()}[*]{tag.info} DES::Decrypted {tag.id}{dataFile.name}{tag.close}")
                return plaintext

            except Exception as e:
                print(f"{tag.error.b()}[-] ERROR:{tag.error} Decryption failed.{tag.close}/r/n{e}")
                raise e

        except Exception as e:
            print(f"{tag.error.b()}[-] ERROR:{tag.error} DES instance failed to initialize.{tag.close}/r/n{e}")
            raise e

    @staticmethod
    def decryptionb(data:bytes, key:bytes):
        global _latest_op_time
        _latest_op_time = 0.0
        try:
            des_instance = custom_enc.des(key[:8])
            print(f"{tag.info.b()}[*]{tag.info} DES::Decrypting: {tag.id}{data}{tag.close}")

            try:

                _latest_op_time = time.perf_counter()
                plaintext = des_instance.decrypt(data, padmode=custom_enc.PAD_PKCS5)
                _latest_op_time = time.perf_counter() - _latest_op_time

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
            print(f"{tag.info.b()}[*]{tag.info} Decrypting: {tag.id}{data}{tag.close}")

            try:

                _latest_op_time = time.perf_counter()
                plaintext = des_instance.decrypt(data.encode(), padmode=custom_enc.PAD_PKCS5)
                _latest_op_time = time.perf_counter() - _latest_op_time

                return plaintext

            except Exception as e:
                print(f"{tag.error.b()}[-] ERROR:{tag.error} Decryption failed.{tag.close}/r/n{e}")
                raise e

        except Exception as e:
            print(f"{tag.error.b()}[-] ERROR:{tag.error} DES instance failed to initialize.{tag.close}/r/n{e}")
            raise e

class aes:
    @staticmethod
    def encryption(dataFile, key:bytes):
        global _latest_op_time
        _latest_op_time = 0.0
        try:
            dataFile.seek(0)
            aes_instance = custom_enc.cry_aes.new(key, mode = custom_enc.cry_aes.MODE_EAX)
            # aes_instance = custom_enc.AES(master_key=key[:32])

            print(f"{tag.info.b()}[*]{tag.info} AES::Encrypting: {tag.id}{dataFile.name}{tag.close}")
            try:
                dataFile.seek(0)

                _latest_op_time = time.perf_counter()
                ciphertext = aes_instance.encrypt(plaintext=dataFile.read())
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
            dataFile.seek(0)
            aes_instance = custom_enc.cry_aes.new(key, mode = custom_enc.cry_aes.MODE_EAX)
            # aes_instance = custom_enc.AES(key[:32])

            print(f"{tag.info.b()}[*]{tag.info} AES::Decrypting: {tag.id}{dataFile.name}{tag.close}")

            try:
                dataFile.seek(0)

                _latest_op_time = time.perf_counter()
                plaintext = aes_instance.decrypt(dataFile.read())
                _latest_op_time = time.perf_counter() - _latest_op_time

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

from fernet import Fernet as Fernet

class RC6:

    @staticmethod
    def encrypt(data_file, key:bytes) -> bytes:
        global _latest_op_time
        _latest_op_time = 0.0

        _latest_op_time = time.perf_counter()
    
        data_file.seek(0)
        rc_inst = rc6_class(key, rounds=16)
        ciphertext = b''
        block = data_file.read(16)
        
        while block:

            if len(block) < 16:
                block += b''.join([ b' ' ] * (16 - len(block)))
            
            if len(block) == 16:
                ciphertext += rc_inst.blocks_to_data(rc_inst.encrypt(block))
            block = data_file.read(16)
        
        _latest_op_time = time.perf_counter() - _latest_op_time

        return ciphertext

    @staticmethod
    def decrypt(data_file, key:bytes) -> bytes:
        global _latest_op_time
        _latest_op_time = 0.0
    
        _latest_op_time = time.perf_counter()

        data_file.seek(0)
        rc_inst = rc6_class(key, rounds=16)
        plaintext = b''
        block = data_file.read(16)
        
        while block:

            if len(block) < 16:
                block += b''.join([ b' ' ] * (16 - len(block)))
            
            if len(block) == 16:
                plaintext += rc_inst.blocks_to_data(rc_inst.decrypt(block))
            block = data_file.read(16)
        
        _latest_op_time = time.perf_counter() - _latest_op_time
        
        return plaintext

class fernet:
    @staticmethod
    def encrypt(data_file, key:bytes) -> bytes:
        global _latest_op_time
        _latest_op_time = 0.0
        

        data_file.seek(0)
        URLSafeKey:bytes = b64.urlsafe_b64encode(key[:32])
        _latest_op_time = time.perf_counter()
        fern_inst = Fernet(key=URLSafeKey)
        _latest_op_time = time.perf_counter() - _latest_op_time

        return fern_inst.encrypt(data_file.read())

    @staticmethod
    def decrypt(data_file, key:bytes):
        global _latest_op_time
        _latest_op_time = 0.0
        
        data_file.seek(0)
        URLSafeKey:bytes = b64.urlsafe_b64encode(key[:32])
        _latest_op_time = time.perf_counter()
        fern_inst = Fernet(key=URLSafeKey)
        _latest_op_time = time.perf_counter() - _latest_op_time

        return fern_inst.decrypt(data_file.read())

if __name__ == '__main__':
    pass
    # import sys
    # import base64 as b64
    # # from Crypto.Cipher
    # sys.path.append(__home__)

    # file = open('D:/Projects/Code Stuff/Final Year Project/SDT-pythonic/client-side/metadata/key.key', 'rb')
    # key = file.read()[:32]
    # file.close()

    # dat_file = open("D:/Projects/Code Stuff/Final Year Project/SDT-pythonic/client-side/metadata/config.json", 'rb')

    # dat_file.flush()

    # rc_e = rc6_class(key, rounds= 16)
    
    # enc = dat_file.read()
    # print('plain\n', enc)
    # # nkey = b64.urlsafe_b64encode(key[:32])
    # print('key\n', key)
    # dat_file.seek(0)

    # ct = b''
    # block = dat_file.read(16)
    
    # while block:

    #     if len(block) < 16:
    #         block += b''.join([ b' ' ] * (16 - len(block)))
        
    #     if len(block) == 16:
    #         ct += rc_e.blocks_to_data(rc_e.encrypt(block))
    #     block = dat_file.read(16)

    # print('ciphertext\n', ct)
    # rc_d = rc6_class(key, rounds= 16)

    # i = 0
    # block = ct[i : i + 16]
    # pt = b''

    # while block:

    #     if len(block) < 16:
    #         block += b''.join([ b' ' ] * (16 - len(block)))
        
    #     if len(block) == 16:
    #         pt += rc_d.blocks_to_data(rc_d.decrypt(block))
        
    #     i += 16
    #     block = ct[i : i + 16]
    # # ct = rc_e.blocks_to_data(rc_e.encrypt(enc))
    # # pt = rc_e.blocks_to_data(rc_e.decrypt(block))
    # print('decrypted\n', pt)

    # # f1 = fernet.Fernet(key=nkey)
    # # enc = f.encrypt(dat_file.read())
    # # dat_file.seek(0)
    # # enc = f1.encrypt(dat_file.read())
    # # print('enc\n', enc)
    
    # # dat_file.close()

    # # with open('weird', 'wb') as encr:
    # #     encr.write(enc)

    # f2 = fernet.Fernet(key=nkey)
    # with open('weird', 'rb') as dencr:
    #     dec = f2.decrypt(dencr.read())
    #     print('dec\n', dec)
    # enc = aes.encryption(dataFile=dat_file, key=key)
    # enc = aes.encryption(dat_file, key=key)



    # enc = _aes.encrypt_block(enc)
    # print(enc)
    # enc = _aes.decrypt_block(enc)

    dat_file.close()