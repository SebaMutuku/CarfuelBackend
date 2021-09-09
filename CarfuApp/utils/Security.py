import base64
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Protocol.KDF import PBKDF2
import random

from CarfuelBackEnd import settings


class AESEncryption:
	password = None

	
	unpad = lambda s: s[:-ord(s[len(s) - 1:])]
	
	def __str__(self, password):
		self.password = "tH!S1sMyT3sTP@SsW0rD"
		return password
	
	def generateKey(self):
		return base64.b64decode(settings.USER_PASS_KEY)
	
	def pad(self, s):
		return  lambda s: s + (settings.ENCRYPTION_BLOCK_SIZE - len(s) % settings.ENCRYPTION_BLOCK_SIZE) * settings.PADDING
	
	def encrypt_value(self,raw_value):
		pad = lambda s: s + (settings.ENCRYPTION_BLOCK_SIZE - len(s) % settings.ENCRYPTION_BLOCK_SIZE) * settings.PADDING
		encode = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
		secret = base64.b64decode(settings.USER_PASS_KEY)
		cipher = AES.new(secret)
		encoded_string=encode(cipher, raw_value)[1:].decode("ascii")
		return encoded_string
		
	
	def decrypt_value(self,encryptedValue):
		secret = base64.b64decode(settings.USER_PASS_KEY)
		decode = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(settings.PADDING)
		cipher = AES.new(secret)
		decoded_string = decode(cipher, encryptedValue)
		print(f"This is the encoded String {decoded_string}")
		return decodeString
