# import binascii
#
# from crypto.Cipher import PKCS1_OAEP
# from crypto.PublicKey import RSA
#
# from CarfuelBackEnd import settings
#
#
# class AESEncryption:
#
#     @staticmethod
#     def generate_rsa_keys():
#         key_pair = RSA.generate(3072)
#         with open('../../staticfiles/keys/publicKey.pem', 'wb') as file:
#             file.write(key_pair.publickey().exportKey(format='PEM'))
#             file.close()
#         with open('../../staticfiles/keys/privateKey.pem', 'wb') as file:
#             file.write(key_pair.exportKey(format='PEM'))
#             file.close()
#
#     @staticmethod
#     def load_public_key():
#         with open(settings.PUBLIC_KEY_NAME, 'rb') as file:
#             public_key = RSA.import_key(file.read())
#             return public_key
#
#     @staticmethod
#     def load_private_key():
#         with open(settings.PRIVATE_KEY_NAME, 'rb') as file:
#             private_key = RSA.importKey(file.read())
#             return private_key
#
#     def encrypt_rsa(self, plain_string):
#         algo = PKCS1_OAEP.new(self.load_public_key())
#         encrpted_string = algo.encrypt(plain_string.encode("utf-8"))
#         return bytes.decode(binascii.b2a_base64(encrpted_string))
#
#     def decrypt_rsa(self, encoded_string, raw_password):
#         try:
#             byte_string = bytes(encoded_string, "utf-8")
#             base_64_decoded_string = binascii.a2b_base64(byte_string)
#             algo = PKCS1_OAEP.new(self.load_private_key())
#             decoded_string = algo.decrypt(base_64_decoded_string)
#             return True if bytes.decode(decoded_string).strip() == raw_password else False
#         except Exception as e:
#             print(e.args)
#             return False
