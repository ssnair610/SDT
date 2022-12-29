"""
"""

import hashlib
import chilkat
import time
import logging

hash_logger = logging.getLogger("Hashing function logger")
hash_logger.propagate = False
hash_logger.setLevel(logging.INFO)
if not hash_logger.handlers:
    fh = logging.FileHandler(filename='hashhistory.log')
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
    fh.setFormatter(formatter)
    hash_logger.addHandler(fh)


hash_sizes = {
    'SHA1' : 40,
    'MD5' : 32,
    'SHA256' : 64,
    'HAVAL' : 44,
    'SNEFRU' : 0
}

_latest_op_time:float = 1.0

# 40 units
class sha_1():
    def __init__(self) -> None:
        self.res = ""

    @staticmethod
    def hash_file(filename):
        global _latest_op_time
        _latest_op_time = time.perf_counter()

        hasher = hashlib.new('sha1')
        hash_logger.info("SHA-1 Hashing function for files invoked")
        with open(filename,"rb") as f:
            block = f.read(512)
            
            while block:
                hasher.update(block)
                block = f.read(512)
        hash_logger.info("SHA-1 Hashing for files terminated.")
        _latest_op_time = time.perf_counter() - _latest_op_time
        return hasher.hexdigest()
    # def hash_file(self, filename):
    #     with open(filename,"rb") as f:
    #         for byte_block in iter(lambda: f.read(4096), b""):
    #             hashlib.sha1.update(byte_block)
    #         self.res = hashlib.sha1.hexdigest()
    #         return self.res
    
    @staticmethod
    def hash_bytes(a_bytes):
        global _latest_op_time
        _latest_op_time = time.perf_counter()
        hasher = hashlib.new('sha1')
        hash_logger.info("SHA-1 Logger for Byte format invoked.")
        for byte_index in range(0, len(a_bytes), 512):
            block = a_bytes[byte_index: byte_index + 512]
            hasher.update(block)

        hash_logger.info("SHA-1 for bytes terminated.")
        _latest_op_time = time.perf_counter() - _latest_op_time
        return hasher.hexdigest()

    @staticmethod
    def hash_unicode(a_string):
        global _latest_op_time
        hash_logger.info("SHA-1 Encoding invoked.")
        _latest_op_time = time.perf_counter()
        hashcode = hashlib.sha1(a_string.encode('utf-8')).hexdigest()
        _latest_op_time = time.perf_counter() - _latest_op_time
        hash_logger.info("SHA-1 encoding terminated.")
        return hashcode
        
    # def DigestSize(self):
    #     return self.res.digest_size
    
    # def BlockSize(self):
    #     return self.res.block_size

# 32 units
class md_5():
    def __init__(self) -> None:
        self.res = ""

    @staticmethod
    def hash_file(filename) -> str:
        global _latest_op_time
        hash_logger.info("MD5 hash invoked for files.")
        _latest_op_time = time.perf_counter()
        hasher = hashlib.new('md5')

        with open(filename,"rb") as f:
            block = f.read(512)

            while block:
                hasher.update(block)
                block = f.read(512)

            f.close()

        _latest_op_time = time.perf_counter() - _latest_op_time
        hash_logger.info("MD5 hash for files terminated.")
        return hasher.hexdigest()

    @staticmethod
    def hash_bytes(a_bytes) -> str:
        global _latest_op_time
        hash_logger.info("MD5 hash for bytes invoked.")
        _latest_op_time = time.perf_counter()
        hasher = hashlib.new('md5')

        for byte_index in range(0, len(a_bytes), 512):
            block = a_bytes[byte_index: byte_index + 512]
            hasher.update(block)

        _latest_op_time = time.perf_counter() - _latest_op_time
        hash_logger.info("MD5 hash for bytes terminated.")
        return hasher.hexdigest()
    # def hash_file(self, filename):
    #     with open(filename,"rb") as f:
    #         for byte_block in iter(lambda: f.read(4096), b""):
    #             hashlib.md5.update(byte_block)
    #         self.res = hashlib.md5.hexdigest()
    #         return self.res
    
    @staticmethod
    def hash_unicode(a_string):
        hash_logger.info("MD5 encoder invoked.")
        global _latest_op_time
        _latest_op_time = time.perf_counter()
        hashcode = hashlib.md5(a_string.encode('utf-8')).hexdigest()
        _latest_op_time = time.perf_counter() - _latest_op_time
        hash_logger.info("MD5 encoder terminated.")
        return hashcode
        
    # def DigestSize(self):
    #     return self.res.digest_size
    
    # def BlockSize(self):
    #     return self.res.block_size
    
# 64 units
class sha_256():
    def __init__(self) -> None:
        self.res = ""

    @staticmethod
    def hash_file(filename):
        global _latest_op_time
        hash_logger.info("SHA-256 hash for files invoked.")
        _latest_op_time = time.perf_counter()
        hasher = hashlib.new('sha256')

        with open(filename,"rb") as f:
            block = f.read(512)
            
            while block:
                hasher.update(block)
                block = f.read(512)

        _latest_op_time = time.perf_counter() - _latest_op_time
        hash_logger.info("SHA-256 hash for files terminated.")
        
        return hasher.hexdigest()

    @staticmethod
    def hash_bytes(a_bytes) -> str:
        global _latest_op_time
        hash_logger.info("SHA-256 hash bytes invoked.")
        _latest_op_time = time.perf_counter()
        hasher = hashlib.new('sha256')

        for byte_index in range(0, len(a_bytes), 512):
            block = a_bytes[byte_index: byte_index + 512]
            hasher.update(block)

        _latest_op_time = time.perf_counter() - _latest_op_time
        hash_logger.info("SHA-256 hash bytes terminated.")
        return hasher.hexdigest()
    

    @staticmethod
    def hash_unicode(a_string):
        global _latest_op_time
        hash_logger.info("SHA-256 hash encoder invoked.")
        _latest_op_time = time.perf_counter()
        hashcode = hashlib.sha256(a_string.encode('utf-8')).hexdigest()
        _latest_op_time = time.perf_counter() - _latest_op_time
        hash_logger.info("SHA-256 hash encoder terminated.")
        return hashcode
        
    # def DigestSize(self):
    #     return self.res.digest_size
    
    # def BlockSize(self):
    #     return self.res.block_size

class haval():
    def __init__(self) -> None:
        self.res = ""

    @staticmethod
    def hash_file(filename) -> str:
        global _latest_op_time
        hash_logger.info("HAVAL hash file invoked.")
        _latest_op_time = time.perf_counter()
        hashfunc = chilkat.CkCrypt2()

        hashfunc.put_HashAlgorithm("haval")
        hashfunc.put_EncodingMode("Base64")
        hashfunc.put_HavalRounds(5)
        hashfunc.put_KeyLength(256)

        hash = hashfunc.hashFileENC(filename)

        # with open(filename,"rb") as file:
        #     block = file.read(512)
        #     hash = ""
        #     while block:
        #         hash_str = ''
        #         hashfunc.HashBytes(block, hash_str) #hashBytes?
        #         # hash_str = hashfunc.hashStringENC(block) #hashBytes?
        #         block = file.read(512)
        #         hash += hash_str

        _latest_op_time = time.perf_counter() - _latest_op_time
        hash_logger.info("HAVAL hash file terminated.")
        return hash
    
    @staticmethod
    def hash_bytes(a_bytes) -> str:
        global _latest_op_time
        hash_logger.info("HAVAL hash bytes invoked.")
        _latest_op_time = time.perf_counter()
        hashfunc = chilkat.CkCrypt2()

        hashfunc.put_HashAlgorithm("haval")
        hashfunc.put_EncodingMode("Base64")
        hashfunc.put_HavalRounds(5)
        hashfunc.put_KeyLength(256)

        hash = ""

        for byte_index in range(0, len(a_bytes), 512):
            block = a_bytes[byte_index: byte_index + 512]
            hash += hashfunc.hashBytesENC(block)

        _latest_op_time = time.perf_counter() - _latest_op_time
        hash_logger.info("HAVAL hash bytes terminated.")
        return hash