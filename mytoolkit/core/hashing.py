"""
"""

import hashlib

class sha_1():
    def __init__(self) -> None:
        self.res = ""

    @staticmethod
    def hash_file(filename):
        hasher = hashlib.new('sha1')

        with open(filename,"rb") as f:
            block = f.read(512)
            
            while block:
                hasher.update(block)
                block = f.read(512)

        return hasher.hexdigest()
    # def hash_file(self, filename):
    #     with open(filename,"rb") as f:
    #         for byte_block in iter(lambda: f.read(4096), b""):
    #             hashlib.sha1.update(byte_block)
    #         self.res = hashlib.sha1.hexdigest()
    #         return self.res
    
    @staticmethod
    def hash_unicode(a_string):
        return hashlib.sha1(a_string.encode('utf-8')).hexdigest()
        
    # def DigestSize(self):
    #     return self.res.digest_size
    
    # def BlockSize(self):
    #     return self.res.block_size

class md_5():
    def __init__(self) -> None:
        self.res = ""

    @staticmethod
    def hash_file(filename) -> str:
        hasher = hashlib.new('md5')

        with open(filename,"rb") as f:
            block = f.read(512)

            while block:
                hasher.update(block)
                block = f.read(512)

            f.close()

        return hasher.hexdigest()
    # def hash_file(self, filename):
    #     with open(filename,"rb") as f:
    #         for byte_block in iter(lambda: f.read(4096), b""):
    #             hashlib.md5.update(byte_block)
    #         self.res = hashlib.md5.hexdigest()
    #         return self.res
    
    @staticmethod
    def hash_unicode(a_string):
        return hashlib.md5(a_string.encode('utf-8')).hexdigest()
        
    # def DigestSize(self):
    #     return self.res.digest_size
    
    # def BlockSize(self):
    #     return self.res.block_size
    
class sha_256():
    def __init__(self) -> None:
        self.res = ""

    @staticmethod
    def hash_file(filename):
        hasher = hashlib.new('sha256')

        with open(filename,"rb") as f:
            block = f.read(512)
            
            while block:
                hasher.update(block)
                block = f.read(512)

        return hasher.hexdigest()
    
    @staticmethod
    def hash_unicode(a_string):
        return hashlib.sha256(a_string.encode('utf-8')).hexdigest()
        
    # def DigestSize(self):
    #     return self.res.digest_size
    
    # def BlockSize(self):
    #     return self.res.block_size