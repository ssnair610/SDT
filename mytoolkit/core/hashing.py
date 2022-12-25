"""
"""

import hashlib
import chilkat

hash_sizes = {
    'SHA1' : 40,
    'MD5' : 32,
    'SHA256' : 64
}

# 40 units
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

# 32 units
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

    @staticmethod
    def hash_bytes(a_bytes) -> str:
        hasher = hashlib.new('md5')

        for byte_index in range(0, len(a_bytes), 512):
            block = a_bytes[byte_index: byte_index + 512]
            hasher.update(block)

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
    
# 64 units
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

class haval():
    def __init__(self) -> None:
        self.res = ""

        @staticmethod
        def hash_file(filename):
            hashfunc = chilkat.CkCrypt2()

            hashfunc.put_HashAlgorithm("haval")
            hashfunc.put_EncodingMode("Base64")
            hashfunc.put_HavalRounds(5)
            hashfunc.put_KeyLength(256)

            with open(filename,"rb") as f:
                block = f.read(512)
                hesh = ""
                while block:
                    hesh_str = hashfunc.hashStringENC(block) #hashBytes?
                    block = f.read(512)
                    hesh += hesh_str
            
            return hesh