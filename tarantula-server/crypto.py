from Crypto.PublicKey import RSA
from Crypto import Random
from base64 import b64decode
from Crypto.Cipher import PKCS1_OAEP
import base64

def read_public_key(key_file):
    key = open(key_file, "r").read().replace("-----BEGIN PUBLIC KEY-----", "").replace("-----END PUBLIC KEY-----", "").replace("\n", "")
    return key

def read_private_key(key_file):
    key = open(key_file, "r").read().replace("-----BEGIN RSA PRIVATE KEY-----", "").replace("-----END RSA PRIVATE KEY-----", "").replace("\n", "")
    return key

def rsa_decrypt(cipherData, crypt_key):
    key = b64decode(crypt_key)
    key = RSA.importKey(key)

    cipher = PKCS1_OAEP.new(key)
    plaintext = cipher.decrypt(b64decode(cipherData))
    return plaintext

def generate_rsa_key_pairs(key_length = 2048):
    key = RSA.generate(key_length)
    private_key = key.export_key('PEM')
    public_key = key.publickey().exportKey('PEM')
    private_key_file = open(f"private-key.pem", "w")
    private_key_file.write(private_key.decode())
    private_key_file.close()

    public_key_file = open(f"public-key.pub", "w")
    public_key_file.write(public_key.decode())
    public_key_file.close()