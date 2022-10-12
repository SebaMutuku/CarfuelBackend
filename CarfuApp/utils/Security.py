import base64
import hashlib

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

from CarfuelBackEnd import settings

HASH_NAME = "SHA256"
IV_LENGTH = 16
ITERATION_COUNT = 65536
KEY_LENGTH = 32


class AESEncryption:
    @staticmethod
    def pad(s): return s + (IV_LENGTH - len(s) % IV_LENGTH) * chr(IV_LENGTH - len(s) % IV_LENGTH)

    @staticmethod
    def unpad(s): return s[0:-ord(s[-1:])]

    @staticmethod
    def get_secret_key(password, salt):
        return hashlib.pbkdf2_hmac(HASH_NAME, password.encode(), salt.encode(), ITERATION_COUNT, KEY_LENGTH)

    def encrypt(self, plain_string):
        secret = self.get_secret_key(settings.ENC_SECRET_KEY, settings.ENC_SALT)
        message = self.pad(plain_string)
        iv = get_random_bytes(IV_LENGTH)
        cipher = AES.new(secret, AES.MODE_CBC, iv)
        cipher_bytes = base64.b64encode(iv + cipher.encrypt(message.encode("utf8")))
        return bytes.decode(cipher_bytes)

    def decrypt(self, encrypted_string):
        secret = self.get_secret_key(settings.ENC_SECRET_KEY, settings.ENC_SALT)
        decoded = base64.b64decode(encrypted_string)
        iv = decoded[:AES.block_size]
        cipher = AES.new(secret, AES.MODE_CBC, iv)
        original_bytes = self.unpad(cipher.decrypt(decoded[IV_LENGTH:]))
        return bytes.decode(original_bytes)
