from Crypto.PublicKey import RSA
from Crypto import Random
from base64 import b64encode, b64decode
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
import base64
import random

def format_public_key(key: str):
    return key.replace("-----BEGIN PUBLIC KEY-----", "").replace("-----END PUBLIC KEY-----", "").replace("\n", "")

def read_file_list():
    files = open("file-list.taranfls", "r")
    return files.read().splitlines()

def read_encrypted_key():
    key = open("encrypted-key.tarankey", "r").read()
    return key

def rsa_encrypt(plainData, crypt_key):
    key = b64decode(crypt_key)
    key = RSA.importKey(key)
        
    cipher = PKCS1_OAEP.new(key)
    ciphertext = b64encode(cipher.encrypt(bytes(plainData, "utf-8")))
    return ciphertext

def read_public_key(key_file):
    key = open(key_file, "r").read().replace("-----BEGIN PUBLIC KEY-----", "").replace("-----END PUBLIC KEY-----", "").replace("\n", "")
    return key

def read_private_key(key_file):
    key = open(key_file, "r").read().replace("-----BEGIN RSA PRIVATE KEY-----", "").replace("-----END RSA PRIVATE KEY-----", "").replace("\n", "")
    return key

def random_string(length):
    # possibilitis: numbers, capital letters, lowercase letters, special characters
    possible_characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+-=[]{}|;':,./<>?"
    _str = ""
    for i in range(length):
        _str += random.choice(possible_characters)
    return _str

def generate_aes_key(key_length):
    return random_string(key_length)

def aes_decrypt(ciphertext, key):
    enc = b64decode(ciphertext)
    iv = enc[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[16:]), AES.block_size)

def aes_encrypt(raw, aes_key):
    raw = pad(raw, AES.block_size)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    return b64encode(iv + cipher.encrypt(raw))

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