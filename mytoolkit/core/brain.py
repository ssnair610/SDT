"""
"""

from pathlib import Path as Path
import mytoolkit.core.hashing as hasher
import mytoolkit.core.keymaker as keymaker
import mytoolkit.core.encrypting as encrypter
# import time	
import shutil
import json
import sys
import os

__home__ = os.path.dirname(__file__)
sys.path.append(os.path.dirname(__home__))

from mytoolkit.txttag import TextTag as tag

__analysis_dir__ = os.path.dirname(os.path.dirname(__home__)) + '/server-side/analysis.json'

class fileThinker:
	def __init__(self, sourceFile:str, targetFile:str, createKey = False, asymmetricKey = False, keyAddress:str = '', name = '') -> None:
		if name == '':
			self.__name = sourceFile + ":" + targetFile
		else:
			self.__name = name

		self.ponder(questionFile=sourceFile, answerFile=targetFile, createKey=createKey, asymmetricKey=asymmetricKey, keyAddress=keyAddress)
		self.__dur = {
			'E0': 0.0,
			'E1': 0.0,
			'H0': 0.0
		}

	def ponder(self, questionFile:str, answerFile:str, createKey = False, asymmetricKey = False, keyAddress:str = '') -> None:
		try:
			shutil.copyfile(questionFile, answerFile)

			if keyAddress != '' and keyAddress[-1] not in ('/', '\\'):
				keyAddress += '/'

			if createKey:
				self.__kaddr:str = keymaker.generateAtDir(os.path.dirname(questionFile), asym=asymmetricKey) if keyAddress == '' else keymaker.generateAtDir(keyAddress if keyAddress[-1] == '/' else keyAddress + '/', asym=asymmetricKey)				
			else:
				self.__kaddr:str = keyAddress + 'privkey.pem' if asymmetricKey else keyAddress + 'key.key'

			self.__tgt = open(answerFile, 'ab+')
			# self.__dat:bytes = self.__tgt.read()
			self.__hashcode:bytes = b''

		except Exception as e:
			print(f'\r\n{tag.error.b()}[-] ERROR:{tag.error} {tag.id.b()}question(){tag.error} encountered exception in {tag.id.b()}{__file__}{tag.close}\r\n{e}')
			raise e
	
	# def enforce(self, contract:dict) -> None:
	def think(self, contract:dict) -> None:
		try:
			if contract['E0'] != 'Rabin':
				self.hash(mode=contract['H0'])
				self.__dur['H0'] = hasher._latest_op_time
				hasher._latest_op_time = 0.0

				self.encrypt(mode=contract['E0'])
				self.__dur['E0'] = encrypter._latest_op_time
				encrypter._latest_op_time = 0.0

				self.encrypt(mode=contract['E1'])
				self.__dur['E1'] = encrypter._latest_op_time
				encrypter._latest_op_time = 0.0
			else:
				
			self.conclude()
		except KeyError as e:
			print(f'\r\n{tag.error.b()}[-] ERROR:{tag.error} Contract incomplete. Can not find term {tag.info.b()}{e}{tag.close}\r\n')
			raise e

		except Exception as e:
			print(f'\r\n{tag.error.b()}[-] ERROR:{tag.error} {tag.id.b()}enforce(){tag.error} encountered exception in {tag.id.b()}{__file__}{tag.close}\r\n{e}')
			raise e

	def unthink(self, contract:dict) -> bool:
		try:
			hash_size:int = hasher.hash_sizes[contract['H0']]
			hashlesssize:int = self.__tgt.seek(-hash_size, os.SEEK_END)
			hashcode:bytes = self.__tgt.read(hash_size)

			print(f'{tag.info.b()}Hash code from file: {tag.id}{hashcode}{tag.close}')

			self.__tgt.seek(0)
			self.__tgt.truncate(hashlesssize)
			self.__tgt.flush()

			self.decrypt(mode=contract['E1'])
			self.__dur['E1'] = encrypter._latest_op_time
			encrypter._latest_op_time = 0.0

			self.decrypt(mode=contract['E0'])
			self.__dur['E0'] = encrypter._latest_op_time
			encrypter._latest_op_time = 0.0
			
			self.hash(mode=contract['H0'])
			self.__dur['H0'] = hasher._latest_op_time
			hasher._latest_op_time = 0.0

			print(f'{tag.info.b()}Hash code generated: {tag.id}{self.__hashcode}{tag.close}')

			self.conclude(append_hash=False)

			return hashcode == self.__hashcode

		except KeyError as e:
			print(f'\r\n{tag.error.b()}[-] ERROR:{tag.error} Contract incomplete. Can not find term {tag.info.b()}{e}{tag.close}\r\n')
			raise e

		except Exception as e:
			print(f'\r\n{tag.error.b()}[-] ERROR:{tag.error} {tag.id.b()}think(){tag.error} encountered exception in {tag.id.b()}{__file__}{tag.close}\r\n{e}')
			raise e

	def keyAddr(self) -> str:
		return self.__kaddr

	def giveKeyAddr(self, key:str) -> None:
		self.__kaddr = key

	def isValidQuestion(self, contract:dict) -> bool:

		try:
			cipher_size = 0
			# cipher_size = self.__tgt.seek(-hash_size, os.SEEK_END)
			# hashcode = self.__tgt.read(hash_size)

			hash_size = hasher.hash_sizes[contract['H0']]
			# find hash_size based on hashing algorithm
			cipher_size = self.__tgt.seek(-hash_size, os.SEEK_END)
			self.__hashcode = self.__tgt.read(hash_size)
			# hash_size = len(self.__hashcode)

			print(f'{tag.info.b()}Hash code from file: {tag.id}{self.__hashcode}{tag.close}')

			self.__tgt.seek(0)
			ciphertext = self.__tgt.read(cipher_size)
			
			print(f"\r\n{tag.info}ciphertext: {tag.id}{ciphertext}{tag.close}")
			plaintext = self.decryptb(self.decryptb(ciphertext, mode=contract['E1']), mode=contract['E0'])
			# print(f"\r\n{tag.info}plaintext: {tag.id}{plaintext}{tag.close}")
			hasheddata = self.hashb(plaintext, mode=contract['H0'])
			print(f"\r\n{tag.info}hashed data: {tag.id}{hasheddata}{tag.close}")
			# print(f"\r\n{tag.info}hashcode: {tag.id}{hashcode}{tag.close}")

			return hasheddata == self.__hashcode

		except Exception as e:
			print(f'\r\n{tag.error.b()}[-] ERROR:{tag.error} {tag.id.b()}isValidQuestion(){tag.error} encountered exception in {tag.id.b()}{__file__}{tag.close}\r\n{e}')
			raise e
		
	def encryptb(self, plaintext:bytes, mode:str):
		if mode == 'None':
			return b''

		# print(f"{tag.info.b()}[@@]{tag.info} plaintext unicode: {tag.id}{plaintext_unicode}{tag.close}")
		ciphertext = plaintext
		key = keymaker.getFromFile(self.__kaddr)
		
		try:
			if mode == 'DES':
				ciphertext = encrypter.des.encryptionb(plaintext, key)
			elif mode == 'AES':
				pass
			else:
				pass
	
			return ciphertext
		
		except Exception as e:
			print(f'\r\n{tag.error.b()}[-] ERROR:{tag.error} {tag.id.b()}encryptb(){tag.error} encountered exception in {tag.id.b()}{__file__}{tag.close}\r\n{e}')
			raise e
		

	def decryptb(self, ciphertext:bytes, mode:str) -> bytes:
		if mode == 'None':
			return b''
		
		# print(f"{tag.id}mode{tag.info}={tag.id}{mode}{tag.close}")
		# print(f"{tag.info.b()}[@@]{tag.info} ciphertext: {tag.id}{ciphertext}{tag.close}")
		plaintext = ciphertext
		key = keymaker.getFromFile(self.__kaddr)

		try:
			if mode == 'DES':
				plaintext = encrypter.des.decryptionb(ciphertext, key)
			if mode == 'AES':
				pass
			else:
				pass

			# print(f"{tag.info.b()}[@@]{tag.info} plaintext: {tag.id}{plaintext}{tag.close}")
			return plaintext

		except Exception as e:
			print(f'\r\n{tag.error.b()}[-] ERROR:{tag.error} {tag.id.b()}decryptb(){tag.error} encountered exception in {tag.id.b()}{__file__}{tag.close}\r\n{e}')
			raise e

	def hashb(self, plaintext:bytes, mode:str) -> bytes:

		hashcode:str = ''

		try:
			if mode == 'MD5':
				hashcode = hasher.md_5.hash_bytes(plaintext)
			elif mode == 'SHA1':
				hashcode = hasher.sha_1.hash_bytes(plaintext)
			elif mode == 'SHA256':
				hashcode = hasher.sha_256.hash_bytes(plaintext)
			elif mode == 'HAVAL':
				hashcode = hasher.haval.hash_bytes(plaintext)

			return hashcode.encode()

		except Exception as e:
			print(f'\r\n{tag.error.b()}[-] ERROR:{tag.error} {tag.id.b()}hashb(){tag.error} encountered exception in {tag.id.b()}{__file__}{tag.close}\r\n{e}')
			raise e

	def encrypt(self, mode) -> None:
		if mode == 'None':
			return

		print(f'\r\n{tag.info.b()}[*]{tag.info} Encrypting to {tag.id}{self.__tgt.name}{tag.info} with {tag.id}{mode}{tag.close}')

		try:
			key = keymaker.getFromFile(self.__kaddr)
			ciphertext = None
			self.__tgt.seek(0)

			if mode == 'DES':
				ciphertext = encrypter.des.encryption(self.__tgt, key=key)
			elif mode == 'AES':
				ciphertext = encrypter.aes().decryption(dataFile=self.__tgt, key=key)
			else:
				pass
				# raise KeyError(f'Hashing mode not supported/recognized.')

			if ciphertext is not None:
				self.__tgt.truncate(0)
				# self.__dat = ciphertext
				self.__tgt.write(ciphertext)
				self.__tgt.flush()

				print(f'\r\n{tag.info.b()}[+]{tag.info} Encryption done.{tag.close}')

		except Exception as e:
			print(f'\r\n{tag.error.b()}[-] ERROR:{tag.error} {tag.id.b()}encrypt(){tag.error} encountered exception in {tag.id.b()}{__file__}{tag.close}\r\n{e}')
			raise e

	def decrypt(self, mode:str) -> None:
		if mode == 'None':
			return

		print(f'\r\n{tag.info.b()}[*]{tag.info} Decrypting to {tag.id}{self.__tgt.name}{tag.info} with {tag.id}{mode}{tag.close}')
		
		try:
			key = keymaker.getFromFile(self.__kaddr)
			plaintext = None

			if mode == 'DES':
				plaintext = encrypter.des.decryption(self.__tgt, key=key)
			elif mode == 'AES':
				plaintext = encrypter.aes().decryption(dataFile=self.__tgt, key=key)
			else:
				pass
				# raise KeyError(f'Hashing mode not supported/recognized.')

			if plaintext is not None:
				self.__tgt.truncate(0)
				self.__tgt.flush()
				self.__tgt.write(plaintext)
				self.__tgt.flush()

				print(f'\r\n{tag.info.b()}[+]{tag.info} Decryption done.{tag.close}')

		except Exception as e:
			print(f'\r\n{tag.error.b()}[-] ERROR:{tag.error} {tag.id.b()}decrypt(){tag.error} encountered exception in {tag.id.b()}{__file__}{tag.close}\r\n{e}')
			raise e

	def hash(self, mode:str) -> None:
		print(f'\r\n{tag.info.b()}[*]{tag.info} Hashing file with {tag.id}{mode}{tag.close}')
		self.__tgt.seek(0)

		try:
			if mode == 'MD5':
				hashcode = hasher.md_5.hash_file(filename=self.__tgt.name)
			elif mode == 'SHA1':
				hashcode = hasher.sha_1.hash_file(filename=self.__tgt.name)
			elif mode == 'SHA256':
				hashcode = hasher.sha_256.hash_file(filename=self.__tgt.name)
			elif mode == 'HAVAL':
				hashcode = hasher.haval.hash_file(filename=self.__tgt.name)
			else:
				print(f'{tag.error.b()}ERROR:{tag.error} Hashing mode not supported/recognized.{tag.close}')
				hashcode = ''

			self.__hashcode = hashcode.encode()
			print('hash size:', len(self.__hashcode))

		except Exception as e:
			print(f'\r\n{tag.error.b()}[-] ERROR:{tag.error} {tag.id.b()}hash(){tag.error} encountered exception in {tag.id.b()}{__file__}{tag.close}\r\n{e}')
			raise e
	
	def conclude(self, append_hash:bool = True) -> None:
		# self.__tgt.truncate(0)
		# self.__tgt.write(self.__dat)
		# self.__tgt.flush()

		if append_hash:
			print(f'\r\n{tag.info.b()}[*]{tag.info} Appending digest to {tag.id}{self.__tgt.name}{tag.close}')
			self.__tgt.seek(0, os.SEEK_END)
			self.__tgt.write(self.__hashcode)
		
		self.__tgt.flush()

		print(f'\r\n{tag.info.b()}[+]{tag.info} Digest appended.{tag.close}')

		analysis_file = open(__analysis_dir__, 'r')
		
		try:
			analysis = json.load(analysis_file)
		except json.JSONDecodeError:
			analysis = dict()

		analysis[self.__name] = self.__dur
		analysis_file.close()


		analysis_file = open(__analysis_dir__, 'w')
		
		json.dump(analysis, analysis_file, indent = 4)

		analysis_file.close()

	def close(self) -> None:
		print(f'\r\n{tag.info.b()}[+]{tag.info} File processing completed.{tag.close}')

		self.__tgt.close()

		print(f'\r\n{tag.info.b()}[+] {tag.id}{self.__tgt.name}{tag.info} closed{tag.close}')