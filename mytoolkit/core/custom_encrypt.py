# import logging as lg
import sys

# import passlib
# from Crypto.Hash import SHA1

py_version = sys.version_info[0]

ECB =	0
CBC =	1

PAD_NORMAL = 1
PAD_PKCS5 = 2

class _baseDes(object):
	def __init__(self, mode=ECB, IV=None, pad=None, padmode=PAD_NORMAL):
		if IV:
			IV = self._guardAgainstUnicode(IV)
		if pad:
			pad = self._guardAgainstUnicode(pad)
		self.block_size = 8

		if pad and padmode == PAD_PKCS5:
			raise ValueError("Cannot use a pad character with PAD_PKCS5")
		if IV and len(IV) != self.block_size:
			raise ValueError("Invalid Initial Value (IV), must be a multiple of " + str(self.block_size) + " bytes")

		self._mode = mode
		self._iv = IV
		self._padding = pad
		self._padmode = padmode

	def getKey(self):
		"""getKey() -> bytes"""
		return self.__key

	def setKey(self, key):
		"""Will set the crypting key for this object."""
		key = self._guardAgainstUnicode(key)
		self.__key = key

	def getMode(self):
		"""getMode() -> pyDes.ECB or pyDes.CBC"""
		return self._mode

	def setMode(self, mode):
		"""Sets the type of crypting mode, pyDes.ECB or pyDes.CBC"""
		self._mode = mode

	def getPadding(self):
		"""getPadding() -> bytes of length 1. Padding character."""
		return self._padding

	def setPadding(self, pad):
		"""setPadding() -> bytes of length 1. Padding character."""
		if pad is not None:
			pad = self._guardAgainstUnicode(pad)
		self._padding = pad

	def getPadMode(self):
		"""getPadMode() -> pyDes.PAD_NORMAL or pyDes.PAD_PKCS5"""
		return self._padmode
		
	def setPadMode(self, mode):
		"""Sets the type of padding mode, pyDes.PAD_NORMAL or pyDes.PAD_PKCS5"""
		self._padmode = mode

	def getIV(self):
		"""getIV() -> bytes"""
		return self._iv

	def setIV(self, IV):
		"""Will set the Initial Value, used in conjunction with CBC mode"""
		if not IV or len(IV) != self.block_size:
			raise ValueError("Invalid Initial Value (IV), must be a multiple of " + str(self.block_size) + " bytes")
		IV = self._guardAgainstUnicode(IV)
		self._iv = IV

	def _padData(self, data, pad, padmode):
		if padmode is None:
			padmode = self.getPadMode()
		if pad and padmode == PAD_PKCS5:
			raise ValueError("Cannot use a pad character with PAD_PKCS5")

		if padmode == PAD_NORMAL:
			if len(data) % self.block_size == 0:
				return data

			if not pad:
				pad = self.getPadding()
			if not pad:
				raise ValueError("Data must be a multiple of " + str(self.block_size) + " bytes in length. Use padmode=PAD_PKCS5 or set the pad character.")
			data += (self.block_size - (len(data) % self.block_size)) * pad
		
		elif padmode == PAD_PKCS5:
			pad_len = 8 - (len(data) % self.block_size)
			if py_version < 3:
				data += pad_len * chr(pad_len)
			else:
				data += bytes([pad_len] * pad_len)

		return data

	def _unpadData(self, data, pad, padmode):
		if not data:
			return data
		if pad and padmode == PAD_PKCS5:
			raise ValueError("Cannot use a pad character with PAD_PKCS5")
		if padmode is None:
			padmode = self.getPadMode()

		if padmode == PAD_NORMAL:
			if not pad:
				pad = self.getPadding()
			if pad:
				data = data[:-self.block_size] + \
					   data[-self.block_size:].rstrip(pad)

		elif padmode == PAD_PKCS5:
			if py_version < 3:
				pad_len = ord(data[-1])
			else:
				pad_len = data[-1]
			data = data[:-pad_len]

		return data

	def _guardAgainstUnicode(self, data):
		if py_version < 3:
			unicode = str
			if isinstance(data, 'unicode'):
				raise ValueError("pyDes can only work with bytes, not Unicode strings.")
		else:
			if isinstance(data, str):
				try:
					return data.encode('ascii')
				except UnicodeEncodeError:
					pass
				raise ValueError("pyDes can only work with encoded strings, not Unicode.")
		return data
	
class des(_baseDes):
	__pc1 = [56, 48, 40, 32, 24, 16,  8,
		  0, 57, 49, 41, 33, 25, 17,
		  9,  1, 58, 50, 42, 34, 26,
		 18, 10,  2, 59, 51, 43, 35,
		 62, 54, 46, 38, 30, 22, 14,
		  6, 61, 53, 45, 37, 29, 21,
		 13,  5, 60, 52, 44, 36, 28,
		 20, 12,  4, 27, 19, 11,  3
	]

	__left_rotations = [
		1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1
	]

	__pc2 = [
		13, 16, 10, 23,  0,  4,
		 2, 27, 14,  5, 20,  9,
		22, 18, 11,  3, 25,  7,
		15,  6, 26, 19, 12,  1,
		40, 51, 30, 36, 46, 54,
		29, 39, 50, 44, 32, 47,
		43, 48, 38, 55, 33, 52,
		45, 41, 49, 35, 28, 31
	]

	__ip = [57, 49, 41, 33, 25, 17, 9,  1,
		59, 51, 43, 35, 27, 19, 11, 3,
		61, 53, 45, 37, 29, 21, 13, 5,
		63, 55, 47, 39, 31, 23, 15, 7,
		56, 48, 40, 32, 24, 16, 8,  0,
		58, 50, 42, 34, 26, 18, 10, 2,
		60, 52, 44, 36, 28, 20, 12, 4,
		62, 54, 46, 38, 30, 22, 14, 6
	]

	__expansion_table = [
		31,  0,  1,  2,  3,  4,
		 3,  4,  5,  6,  7,  8,
		 7,  8,  9, 10, 11, 12,
		11, 12, 13, 14, 15, 16,
		15, 16, 17, 18, 19, 20,
		19, 20, 21, 22, 23, 24,
		23, 24, 25, 26, 27, 28,
		27, 28, 29, 30, 31,  0
	]

	__sbox = [
		# S1
		[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
		 0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
		 4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
		 15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],

		# S2
		[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
		 3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
		 0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
		 13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],

		# S3
		[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
		 13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
		 13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
		 1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],

		# S4
		[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
		 13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
		 10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
		 3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],

		# S5
		[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
		 14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
		 4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
		 11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],

		# S6
		[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
		 10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
		 9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
		 4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],

		# S7
		[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
		 13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
		 1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
		 6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],

		# S8
		[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
		 1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
		 7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
		 2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
	]

	__p = [
		15, 6, 19, 20, 28, 11,
		27, 16, 0, 14, 22, 25,
		4, 17, 30, 9, 1, 7,
		23,13, 31, 26, 2, 8,
		18, 12, 29, 5, 21, 10,
		3, 24
	]

	__fp = [
		39,  7, 47, 15, 55, 23, 63, 31,
		38,  6, 46, 14, 54, 22, 62, 30,
		37,  5, 45, 13, 53, 21, 61, 29,
		36,  4, 44, 12, 52, 20, 60, 28,
		35,  3, 43, 11, 51, 19, 59, 27,
		34,  2, 42, 10, 50, 18, 58, 26,
		33,  1, 41,  9, 49, 17, 57, 25,
		32,  0, 40,  8, 48, 16, 56, 24
	]

	ENCRYPT =	0x00
	DECRYPT =	0x01

	def __init__(self, key, mode=ECB, IV=None, pad=None, padmode=PAD_NORMAL):
		if len(key) != 8:
			raise ValueError("Invalid DES key size. Key must be exactly 8 bytes long.")
		_baseDes.__init__(self, mode, IV, pad, padmode)
		self.key_size = 8

		self.L = []
		self.R = []
		self.Kn = [ [0] * 48 ] * 16	
		self.final = []

		self.setKey(key)

	def setKey(self, key):
		"""Will set the crypting key for this object. Must be 8 bytes."""
		_baseDes.setKey(self, key)
		self.__create_sub_keys()

	def __String_to_BitList(self, data):
		"""Turn the string data, into a list of bits (1, 0)'s"""
		if py_version < 3:
			data = [ord(c) for c in data]
		l = len(data) * 8
		result = [0] * l
		pos = 0
		for ch in data:
			i = 7
			while i >= 0:
				if ch & (1 << i) != 0:
					result[pos] = 1
				else:
					result[pos] = 0
				pos += 1
				i -= 1

		return result

	def __BitList_to_String(self, data):
		"""Turn the list of bits -> data, into a string"""
		result = []
		pos = 0
		c = 0
		while pos < len(data):
			c += data[pos] << (7 - (pos % 8))
			if (pos % 8) == 7:
				result.append(c)
				c = 0
			pos += 1

		if py_version < 3:
			return ''.join([ chr(c) for c in result ])
		else:
			return bytes(result)

	def __permutate(self, table, block):
		"""Permutate this block with the specified table"""
		return list(map(lambda x: block[x], table))

	def __create_sub_keys(self):
		"""Create the 16 subkeys K[1] to K[16] from the given key"""
		key = self.__permutate(des.__pc1, self.__String_to_BitList(self.getKey()))
		i = 0
		self.L = key[:28]
		self.R = key[28:]
		while i < 16:
			j = 0
			while j < des.__left_rotations[i]:
				self.L.append(self.L[0])
				del self.L[0]
				self.R.append(self.R[0])
				del self.R[0]
				j += 1
			self.Kn[i] = self.__permutate(des.__pc2, self.L + self.R)
			i += 1
	def __des_crypt(self, block, crypt_type):
		"""Crypt the block of data through DES bit-manipulation"""
		block = self.__permutate(des.__ip, block)
		self.L = block[:32]
		self.R = block[32:]

		if crypt_type == des.ENCRYPT:
			iteration = 0
			iteration_adjustment = 1
		else:
			iteration = 15
			iteration_adjustment = -1

		i = 0
		while i < 16:
			tempR = self.R[:]

			self.R = self.__permutate(des.__expansion_table, self.R)

			self.R = list(map(lambda x, y: x ^ y, self.R, self.Kn[iteration]))
			B = [self.R[:6], self.R[6:12], self.R[12:18], self.R[18:24], self.R[24:30], self.R[30:36], self.R[36:42], self.R[42:]]

			j = 0
			Bn = [0] * 32
			pos = 0
			while j < 8:
				m = (B[j][0] << 1) + B[j][5]
				n = (B[j][1] << 3) + (B[j][2] << 2) + (B[j][3] << 1) + B[j][4]

				v = des.__sbox[j][(m << 4) + n]

				Bn[pos] = (v & 8) >> 3
				Bn[pos + 1] = (v & 4) >> 2
				Bn[pos + 2] = (v & 2) >> 1
				Bn[pos + 3] = v & 1

				pos += 4
				j += 1

			self.R = self.__permutate(des.__p, Bn)
			self.R = list(map(lambda x, y: x ^ y, self.R, self.L))
			self.L = tempR

			i += 1
			iteration += iteration_adjustment

		self.final = self.__permutate(des.__fp, self.R + self.L)
		return self.final

	def crypt(self, data, crypt_type):
		if not data:
			return ''
		if len(data) % self.block_size != 0:
			if crypt_type == des.DECRYPT: 
				raise ValueError("Invalid data length, data must be a multiple of " + str(self.block_size) + " bytes\n.")
			if not self.getPadding():
				raise ValueError("Invalid data length, data must be a multiple of " + str(self.block_size) + " bytes\n. Try setting the optional padding character")
			else:
				data += (self.block_size - (len(data) % self.block_size)) * self.getPadding()

		if self.getMode() == CBC:
			if self.getIV():
				iv = self.__String_to_BitList(self.getIV())
			else:
				raise ValueError("For CBC mode, you must supply the Initial Value (IV) for ciphering")

		i = 0
		dict = {}
		result = []

		while i < len(data):				
			block = self.__String_to_BitList(data[i:i+8])
			if self.getMode() == CBC:
				if crypt_type == des.ENCRYPT:
					block = list(map(lambda x, y: x ^ y, block, iv))
				processed_block = self.__des_crypt(block, crypt_type)
				if crypt_type == des.DECRYPT:
					processed_block = list(map(lambda x, y: x ^ y, processed_block, iv))
					iv = block
				else:
					iv = processed_block
			else:
				processed_block = self.__des_crypt(block, crypt_type)

			result.append(self.__BitList_to_String(processed_block))
			i += 8

		if py_version < 3:
			return ''.join(result)
		else:
			return bytes.fromhex('').join(result)

	def encrypt(self, data, pad=None, padmode=None):
		data = self._guardAgainstUnicode(data)
		if pad is not None:
			pad = self._guardAgainstUnicode(pad)
		data = self._padData(data, pad, padmode)
		return self.crypt(data, des.ENCRYPT)

	def decrypt(self, data, pad=None, padmode=None):
		data = self._guardAgainstUnicode(data)
		if pad is not None:
			pad = self._guardAgainstUnicode(pad)
		data = self.crypt(data, des.DECRYPT)
		return self._unpadData(data, pad, padmode)

s_box = (
	0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
	0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
	0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
	0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
	0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
	0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
	0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
	0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
	0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
	0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
	0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
	0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
	0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
	0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
	0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
	0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
)

inv_s_box = (
	0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
	0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
	0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
	0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
	0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
	0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
	0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
	0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
	0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
	0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
	0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
	0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
	0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
	0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
	0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
	0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D,
)

class base_aes():
	@staticmethod
	def sub_bytes(s):
		for i in range(4):
			for j in range(4):
				s[i][j] = s_box[s[i][j]]

	@staticmethod
	def inv_sub_bytes(s):
		for i in range(4):
			for j in range(4):
				s[i][j] = inv_s_box[s[i][j]]

	@staticmethod
	def shift_rows(s):
		s[0][1], s[1][1], s[2][1], s[3][1] = s[1][1], s[2][1], s[3][1], s[0][1]
		s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2]
		s[0][3], s[1][3], s[2][3], s[3][3] = s[3][3], s[0][3], s[1][3], s[2][3]

	@staticmethod
	def inv_shift_rows(s):
		s[0][1], s[1][1], s[2][1], s[3][1] = s[3][1], s[0][1], s[1][1], s[2][1]
		s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2]
		s[0][3], s[1][3], s[2][3], s[3][3] = s[1][3], s[2][3], s[3][3], s[0][3]

	@staticmethod
	def add_round_key(s, k):
		for i in range(4):
			for j in range(4):
				s[i][j] ^= k[i][j]

	x_time = lambda a: (((a << 1) ^ 0x1B) & 0xFF) if (a & 0x80) else (a << 1)

	@staticmethod
	def mix_single_column(a) -> None:
		t = a[0] ^ a[1] ^ a[2] ^ a[3]
		u = a[0]
		a[0] ^= t ^ base_aes.x_time(a[0] ^ a[1])
		a[1] ^= t ^ base_aes.x_time(a[1] ^ a[2])
		a[2] ^= t ^ base_aes.x_time(a[2] ^ a[3])
		a[3] ^= t ^ base_aes.x_time(a[3] ^ u)

	@staticmethod
	def mix_columns(s):
		for i in range(4):
			base_aes.mix_single_column(s[i])

	@staticmethod
	def inv_mix_columns(s):
		for i in range(4):
			u = base_aes.x_time(base_aes.x_time(s[i][0] ^ s[i][2]))
			v = base_aes.x_time(base_aes.x_time(s[i][1] ^ s[i][3]))
			s[i][0] ^= u
			s[i][1] ^= v
			s[i][2] ^= u
			s[i][3] ^= v

		base_aes.mix_columns(s)


	r_con = (
		0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40,
		0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A,
		0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A,
		0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39,
	)


	@staticmethod
	def bytes2matrix(text):
		return [list(text[i:i+4]) for i in range(0, len(text), 4)]

	@staticmethod
	def matrix2bytes(matrix):
		return bytes(sum(matrix, []))

	@staticmethod
	def xor_bytes(a, b):
		return bytes(i^j for i, j in zip(a, b))

	@staticmethod
	def inc_bytes(a):
		out = list(a)
		for i in reversed(range(len(out))):
			if out[i] == 0xFF:
				out[i] = 0
			else:
				out[i] += 1
				break
		return bytes(out)

	@staticmethod
	def pad(plaintext):
		padding_len = 16 - (len(plaintext) % 16)
		padding = bytes([padding_len] * padding_len)
		return plaintext + padding

	@staticmethod
	def unpad(plaintext):
		padding_len = plaintext[-1]
		assert padding_len > 0
		message, padding = plaintext[:-padding_len], plaintext[-padding_len:]
		assert all(p == padding_len for p in padding)
		return message

	@staticmethod
	def split_blocks(message, block_size=16, require_padding=True):
			assert len(message) % block_size == 0 or not require_padding
			return [message[i:i+16] for i in range(0, len(message), block_size)]

class AES(base_aes):
	rounds_by_key_size = {16: 10, 24: 12, 32: 14}
	def __init__(self, master_key):
		assert len(master_key) in AES.rounds_by_key_size
		self.n_rounds = AES.rounds_by_key_size[len(master_key)]
		self._key_matrices = self._expand_key(master_key)

	def _expand_key(self, master_key):
		key_columns = base_aes.bytes2matrix(master_key)
		iteration_size = len(master_key) // 4

		i = 1
		while len(key_columns) < (self.n_rounds + 1) * 4:
			word = list(key_columns[-1])

			if len(key_columns) % iteration_size == 0:
				word.append(word.pop(0))
				word = [s_box[b] for b in word]
				word[0] ^= base_aes.r_con[i]
				i += 1
			elif len(master_key) == 32 and len(key_columns) % iteration_size == 4:
				word = [s_box[b] for b in word]
			word = base_aes.xor_bytes(word, key_columns[-iteration_size])
			key_columns.append(word)

		return [key_columns[4*i : 4*(i+1)] for i in range(len(key_columns) // 4)]

	def encrypt_block(self, plaintext):
		assert len(plaintext) == 16

		plain_state = base_aes.bytes2matrix(plaintext)
		base_aes.add_round_key(plain_state, self._key_matrices[0])
		for i in range(1, self.n_rounds):
			base_aes.sub_bytes(plain_state)
			base_aes.shift_rows(plain_state)
			base_aes.mix_columns(plain_state)
			base_aes.add_round_key(plain_state, self._key_matrices[i])

		base_aes.sub_bytes(plain_state)
		base_aes.shift_rows(plain_state)
		base_aes.add_round_key(plain_state, self._key_matrices[-1])

		return base_aes.matrix2bytes(plain_state)

	def decrypt_block(self, ciphertext):
		assert len(ciphertext) == 16
	
		cipher_state = base_aes.bytes2matrix(ciphertext)
		base_aes.add_round_key(cipher_state, self._key_matrices[-1])
		base_aes.inv_shift_rows(cipher_state)
		base_aes.inv_sub_bytes(cipher_state)

		for i in range(self.n_rounds - 1, 0, -1):
			base_aes.add_round_key(cipher_state, self._key_matrices[i])
			base_aes.inv_mix_columns(cipher_state)
			base_aes.inv_shift_rows(cipher_state)
			base_aes.inv_sub_bytes(cipher_state)

		base_aes.add_round_key(cipher_state, self._key_matrices[0])

		return base_aes.matrix2bytes(cipher_state)

	def encrypt_cbc(self, plaintext, iv):
		assert len(iv) == 16
	
		plaintext = base_aes.pad(plaintext)
		blocks = []
		previous = iv
		for plaintext_block in base_aes.split_blocks(plaintext):
			block = self.encrypt_block(base_aes.xor_bytes(plaintext_block, previous))
			blocks.append(block)
			previous = block

		return b''.join(blocks)

	def decrypt_cbc(self, ciphertext, iv):
		assert len(iv) == 16
	
		blocks = []
		previous = iv
		for ciphertext_block in base_aes.split_blocks(ciphertext):
			blocks.append(base_aes.xor_bytes(previous, self.decrypt_block(ciphertext_block)))
			previous = ciphertext_block

		return base_aes.unpad(b''.join(blocks))

	def encrypt_pcbc(self, plaintext, iv):
		assert len(iv) == 16
	
		plaintext = base_aes.pad(plaintext)
		blocks = []
		prev_ciphertext = iv
		prev_plaintext = bytes(16)
		for plaintext_block in base_aes.split_blocks(plaintext):
			ciphertext_block = self.encrypt_block(base_aes.xor_bytes(plaintext_block, base_aes.xor_bytes(prev_ciphertext, prev_plaintext)))
			blocks.append(ciphertext_block)
			prev_ciphertext = ciphertext_block
			prev_plaintext = plaintext_block

		return b''.join(blocks)

	def decrypt_pcbc(self, ciphertext, iv):
		assert len(iv) == 16

		blocks = []
		prev_ciphertext = iv
		prev_plaintext = bytes(16)
		for ciphertext_block in base_aes.split_blocks(ciphertext):
			plaintext_block = base_aes.xor_bytes(base_aes.xor_bytes(prev_ciphertext, prev_plaintext), self.decrypt_block(ciphertext_block))
			blocks.append(plaintext_block)
			prev_ciphertext = ciphertext_block
			prev_plaintext = plaintext_block

		return base_aes.unpad(b''.join(blocks))

	def encrypt_cfb(self, plaintext, iv):
		assert len(iv) == 16

		blocks = []
		prev_ciphertext = iv
		for plaintext_block in base_aes.split_blocks(plaintext, require_padding=False):
			ciphertext_block = base_aes.xor_bytes(plaintext_block, self.encrypt_block(prev_ciphertext))
			blocks.append(ciphertext_block)
			prev_ciphertext = ciphertext_block

		return b''.join(blocks)

	def decrypt_cfb(self, ciphertext, iv):
		assert len(iv) == 16

		blocks = []
		prev_ciphertext = iv
		for ciphertext_block in base_aes.split_blocks(ciphertext, require_padding=False):
			plaintext_block = base_aes.xor_bytes(ciphertext_block, self.encrypt_block(prev_ciphertext))
			blocks.append(plaintext_block)
			prev_ciphertext = ciphertext_block

		return b''.join(blocks)

	def encrypt_ofb(self, plaintext, iv):
		assert len(iv) == 16

		blocks = []
		previous = iv
		for plaintext_block in base_aes.split_blocks(plaintext, require_padding=False):
			block = self.encrypt_block(previous)
			ciphertext_block = base_aes.xor_bytes(plaintext_block, block)
			blocks.append(ciphertext_block)
			previous = block

		return b''.join(blocks)

	def decrypt_ofb(self, ciphertext, iv):
		assert len(iv) == 16

		blocks = []
		previous = iv
		for ciphertext_block in base_aes.split_blocks(ciphertext, require_padding=False):
			block = self.encrypt_block(previous)
			plaintext_block = base_aes.xor_bytes(ciphertext_block, block)
			blocks.append(plaintext_block)
			previous = block

		return b''.join(blocks)

	def encrypt_ctr(self, plaintext, iv):
		assert len(iv) == 16

		blocks = []
		nonce = iv
		for plaintext_block in base_aes.split_blocks(plaintext, require_padding=False):
			block = base_aes.xor_bytes(plaintext_block, self.encrypt_block(nonce))
			blocks.append(block)
			nonce = base_aes.inc_bytes(nonce)

		return b''.join(blocks)

	def decrypt_ctr(self, ciphertext, iv):
		assert len(iv) == 16

		blocks = []
		nonce = iv
		for ciphertext_block in base_aes.split_blocks(ciphertext, require_padding=False):
			block = base_aes.xor_bytes(ciphertext_block, self.encrypt_block(nonce))
			blocks.append(block)
			nonce = base_aes.inc_bytes(nonce)

		return b''.join(blocks)

# from Crypto.PublicKey import ECC
# import sys
# import os

# __home__ = os.path.dirname(__file__)
# sys.path.append(os.path.dirname(os.path.dirname(__home__)))

# from mytoolkit.txttag import TextTag as tag

# file = open("D:\\Projects\\Code Stuff\\Final Year Project\\SDT-pythonic\\server-side\\inbound\\-5099880669623479984\\privkey.pem", 'rt')

# key = ECC.import_key(file.read())
# print(f"{tag.info}Key read: {tag.id}{key.export_key(format='DER')}{tag.close}")

# dfile = open('D:\\Projects\\Code Stuff\\Final Year Project\\SDT-pythonic\\server-side\\inbound\\-5099880669623479984\\dummy.txt')

# _des = des(key.export_key(format='DER')[:8])
# dec = _des.encrypt(dfile.read(), padmode=PAD_PKCS5)
# print(f"{tag.info}{type(dec)}{tag.white}:{tag.id}{dec}{tag.close}")
# dec = _des.decrypt(dec, padmode=PAD_PKCS5).decode()
# print(f"{tag.info}{type(dec)}{tag.white}:{tag.id}{dec}{tag.close}")