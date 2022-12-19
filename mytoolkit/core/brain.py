"""
"""

from pathlib import Path as Path
import mytoolkit.core.hashing as hasher
import mytoolkit.core.keymaker as keymaker
import mytoolkit.core.encrypting as encrypter
import shutil
import sys
import os

__home__ = os.path.dirname(__file__)
sys.path.append(os.path.dirname(__home__))

from mytoolkit.txttag import TextTag as tag

class fileThinker:
	def __init__(self, sourceFile:str, targetFile:str, createKey = True, asymmetricKey = True, keyAddress:str = '') -> None:
		self.ponder(questionFile=sourceFile, answerFile=targetFile, createKey=createKey, assymetricKey=asymmetricKey, keyAddress=keyAddress)

	def ponder(self, questionFile:str, answerFile:str, createKey = True, assymetricKey = False, keyAddress:str = '') -> None:
		try:
			shutil.copyfile(questionFile, answerFile)
			
			if createKey:
				self.__kaddr:str = keymaker.generateAtDir(os.path.dirname(questionFile)) if keyAddress == '' else keymaker.generateAtDir(keyAddress, asym=assymetricKey)
			else:
				self.__kaddr:str = ''

			self.__tgt = open(answerFile, 'ab+')
			self.__hashcode:bytes = b''
		
		except Exception as e:
			print(f'\r\n{tag.error.b()}[-] ERROR:{tag.error} {tag.id.b()}question(){tag.error} encountered exception in {tag.id.b()}{__file__}{tag.close}\r\n{e}')
			raise e
	
	def enforce(self, contract:dict) -> None:
		try:
			self.hash(mode=contract['H0'])
			self.encrypt(mode=contract['E0'])
			self.encrypt(mode=contract['E1'])

			self.conclude()
		except KeyError as e:
			print(f'\r\n{tag.error.b()}[-] ERROR:{tag.error} Contract incomplete. Can not find term {tag.info.b()}{e}{tag.close}\r\n')
			raise e
		
		except Exception as e:
			print(f'\r\n{tag.error.b()}[-] ERROR:{tag.error} {tag.id.b()}enforce(){tag.error} encountered exception in {tag.id.b()}{__file__}{tag.close}\r\n{e}')
			raise e

	def keyAddr(self) -> str:
		return self.__kaddr

	def giveKeyAddr(self, key:str) -> None:
		self.__kaddr = key

	def isValidQuestion(self, contract:dict):

		try:
			cipher_size = 0
			# cipher_size = self.__tgt.seek(-hash_size, os.SEEK_END)
			# hashcode = self.__tgt.read(hash_size)

			if self.__hashcode != b'':
				hash_size = len(self.__hashcode)
				cipher_size = self.__tgt.seek(-hash_size, os.SEEK_END)

			self.__tgt.seek(0)
			ciphertext = self.__tgt.read(cipher_size)
			
			# print(f"\r\n{tag.info}ciphertext: {tag.id}{ciphertext}{tag.close}")
			plaintext = self.decrypts(self.decrypts(ciphertext, mode=contract['E1']), mode=contract['E0'])
			# print(f"\r\n{tag.info}plaintext: {tag.id}{plaintext}{tag.close}")
			hasheddata = self.hashs(plaintext, mode=contract['H0'])
			# print(f"\r\n{tag.info}hashed data: {tag.id}{hasheddata}{tag.close}")
			# print(f"\r\n{tag.info}hashcode: {tag.id}{hashcode}{tag.close}")

			return hasheddata == self.__hashcode

		except Exception as e:
			print(f'\r\n{tag.error.b()}[-] ERROR:{tag.error} {tag.id.b()}isValidQuestion(){tag.error} encountered exception in {tag.id.b()}{__file__}{tag.close}\r\n{e}')
			raise e
		
	def encrypts(self, plaintext:bytes, mode:str):
		
		plaintext_unicode = plaintext.decode()
		# print(f"{tag.info.b()}[@@]{tag.info} plaintext unicode: {tag.id}{plaintext_unicode}{tag.close}")
		ciphertext = plaintext
		key = keymaker.getFromFile(self.__kaddr)
		
		try:
			if mode == 'RSA':
				pass
			elif mode == 'DES':
				ciphertext = encrypter.des.encryptionstr(plaintext_unicode, key)
			if mode == 'AES':
				pass
			else:
				pass
	
			return ciphertext
		
		except Exception as e:
			print(f'\r\n{tag.error.b()}[-] ERROR:{tag.error} {tag.id.b()}encrypts(){tag.error} encountered exception in {tag.id.b()}{__file__}{tag.close}\r\n{e}')
			raise e
		

	def decrypts(self, ciphertext:bytes, mode:str) -> bytes:
		
		# print(f"{tag.id}mode{tag.info}={tag.id}{mode}{tag.close}")
		# print(f"{tag.info.b()}[@@]{tag.info} ciphertext: {tag.id}{ciphertext}{tag.close}")
		plaintext = ciphertext
		key = keymaker.getFromFile(self.__kaddr)

		try:
			if mode == 'RSA':
				pass
			elif mode == 'DES':
				plaintext = encrypter.des.decryptionstr(ciphertext, key)
			if mode == 'AES':
				pass
			else:
				pass

			# print(f"{tag.info.b()}[@@]{tag.info} plaintext: {tag.id}{plaintext}{tag.close}")
			return plaintext
		
		except Exception as e:
			print(f'\r\n{tag.error.b()}[-] ERROR:{tag.error} {tag.id.b()}decrypts(){tag.error} encountered exception in {tag.id.b()}{__file__}{tag.close}\r\n{e}')
			raise e

	def hashs(self, plaintext:bytes, mode:str) -> bytes:

		hashcode:str = ''
		plaintext_unicode = plaintext.decode()

		try:
			if mode == 'MD5':
				hashcode = hasher.md_5.hash_unicode(plaintext_unicode)
			elif mode == 'SHA1':
				hashcode = hasher.sha_1.hash_unicode(plaintext_unicode)
			elif mode == 'SHA256':
				hashcode = hasher.sha_256.hash_unicode(plaintext_unicode)
	
			return hashcode.encode()

		except Exception as e:
			print(f'\r\n{tag.error.b()}[-] ERROR:{tag.error} {tag.id.b()}hashs(){tag.error} encountered exception in {tag.id.b()}{__file__}{tag.close}\r\n{e}')
			raise e			

	def encrypt(self, mode) -> None:
		print(f'\r\n{tag.info.b()}[*]{tag.info} Encrypting to {tag.id}{self.__tgt.name}{tag.info} with {tag.id}{mode}{tag.close}')

		try:
			key = keymaker.getFromFile(self.__kaddr)
			ciphertext = None

			if mode == 'RSA':
				# encrypter.rsa_alg.encrypt()
				pass
				# hashcode = hasher.md_5.hash_file(filename=self.__tgt.name)
			elif mode == 'DES':
				ciphertext = encrypter.des.encryption(self.__tgt, key=key)
			elif mode == 'AES':
				# encrypter.AES.encrypt_block()
				pass
				# hashcode = hasher.sha_256.hash_file(filename=self.__tgt.name)
			else:
				pass
				# raise KeyError(f'Hashing mode not supported/recognized.')

			if ciphertext is not None:
				self.__tgt.truncate(0)
				self.__tgt.write(ciphertext)
				self.__tgt.flush()

				print(f'\r\n{tag.info.b()}[+]{tag.info} Encryption done.{tag.close}')

		except Exception as e:
			print(f'\r\n{tag.error.b()}[-] ERROR:{tag.error} {tag.id.b()}encrypt(){tag.error} encountered exception in {tag.id.b()}{__file__}{tag.close}\r\n{e}')
			raise e

	def decrypt(self, mode:str) -> None:
		print(f'\r\n{tag.info.b()}[*]{tag.info} Decrypting to {tag.id}{self.__tgt.name}{tag.info} with {tag.id}{mode}{tag.close}')

		try:
			key = keymaker.getFromFile(self.__kaddr)
			plaintext = None

			if mode == 'RSA':
				# encrypter.rsa_alg.encrypt()
				pass
				# hashcode = hasher.md_5.hash_file(filename=self.__tgt.name)
			elif mode == 'DES':
				plaintext = encrypter.des.decryption(self.__tgt, key=key)
			elif mode == 'AES':
				# encrypter.AES.encrypt_block()
				pass
				# hashcode = hasher.sha_256.hash_file(filename=self.__tgt.name)
			else:
				pass
				# raise KeyError(f'Hashing mode not supported/recognized.')

			if plaintext is not None:
				plaintext = plaintext.encode()
				self.__tgt.truncate(0)
				# print(f'\r\n{tag.info.b()}[+]{tag.info} plaintext: {tag.id}{plaintext}{tag.close}')
				self.__tgt.write(plaintext)
				self.__tgt.flush()

				print(f'\r\n{tag.info.b()}[+]{tag.info} Decryption done.{tag.close}')

		except Exception as e:
			print(f'\r\n{tag.error.b()}[-] ERROR:{tag.error} {tag.id.b()}decrypt(){tag.error} encountered exception in {tag.id.b()}{__file__}{tag.close}\r\n{e}')
			raise e

	def hash(self, mode:str) -> None:
		print(f'\r\n{tag.info.b()}[*]{tag.info} Hashing file with {tag.id}{mode}{tag.close}')

		try:
			if mode == 'MD5':
				hashcode = hasher.md_5.hash_file(filename=self.__tgt.name)
			elif mode == 'SHA1':
				hashcode = hasher.sha_1.hash_file(filename=self.__tgt.name)
			elif mode == 'SHA256':
				hashcode = hasher.sha_256.hash_file(filename=self.__tgt.name)
			else:
				raise KeyError(f'Hashing mode not supported/recognized.')
				# hashcode = ''

			self.__hashcode = hashcode.encode()

		except Exception as e:
			print(f'\r\n{tag.error.b()}[-] ERROR:{tag.error} {tag.id.b()}hash(){tag.error} encountered exception in {tag.id.b()}{__file__}{tag.close}\r\n{e}')
			raise e
	
	def conclude(self) -> None:
		print(f'\r\n{tag.info.b()}[*]{tag.info} Appending digest to {tag.id}{self.__tgt.name}{tag.close}')
		
		self.__tgt.write(self.__hashcode)
		self.__tgt.flush()
		
		print(f'\r\n{tag.info.b()}[+]{tag.info} Digest appended.{tag.close}')

	def close(self) -> None:
		print(f'\r\n{tag.info.b()}[+]{tag.info} File processing completed.{tag.close}')
		
		self.__tgt.close()
		
		print(f'\r\n{tag.info.b()}[+] {tag.id}{self.__tgt.name}{tag.info} closed and ready for transmission.{tag.close}')