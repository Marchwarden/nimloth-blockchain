from flask import Flask
from dataclasses import dataclass, field
import hashlib
import json
import time
import math
import binascii
import numpy as np
import pandas as pd
import logging
import collections

from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA


app = Flask(__name__)
transactions = []

@dataclass
class User:
    def __init__(self):
        self._private_key = RSA.generate(1024)
        self._public_key = self._private_key.publickey()
        self._signer = pkcs1_15.new(self._private_key)

    @property
    def identity(self):
        return binascii.hexlify(self._public_key.exportKey(format='DER')).decode('ascii')

@dataclass
class Transaction:
    def __init__(self, sender, recipient, value):
        self.sender = sender
        self.recipient = recipient
        self.value = value
        self.time = time.time()

    def to_dict(self):
        if self.sender == "Genesis":
            identity = "Genesis"
        else:
            identity = self.sender.identity
        
        return collections.OrderedDict({
            'sender': identity,
            'recipient': self.recipient,
            'value': self.value,
            'time': self.time })

    def sign_transaction(self):
        private_key = self.sender._private_key
        signer = pkcs1_15.new(private_key)
        h = SHA.new(str(self.to_dict()).encode('utf8'))
        
        return binascii.hexlify(signer.sign(h)).decode('ascii') 

@dataclass
class NimlothBlock:
    previous_block_hash: str
    timestamp: float
    nonce: int = 0 
    transactions_list: list = field(default_factory=list)

    def compute_hash(self) -> str:
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

@dataclass 
class Blockchain:
    unconfirmed_transactions: list = field(default_factory=list)
    chain: list = field(default_factory=list)
    difficulty: int = 2
    
    def __post_init__(self):
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = NimlothBlock(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    def proof_of_work(self, block):
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0'*Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash
    
    def add_block(self, block, proof):
        previous_hash = self.last_block.hash
        if previous_hash != block.previous_hash:
            return False
        if not self.is_valid_proof(block, proof):
            return False
        block.hash = proof
        self.chain.append(block)
        return True

    def is_valid_proof(self, block, block_hash):
        return (block_hash.startswith('0'*Blockchain.difficulty) and 
                block_hash == block.compute_hash())
    
    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    # def mine(self):
    #         if not self.unconfirmed_transactions:
    #             return False
            
    #         last_block = self.last_block

    #         new_block = Block(index = last_block.index + 1,
    #                           transactions = self.unconfirmed_transactions,
    #                           timestamp = time.time(),
    #                           previous_hash=last_block.hash)

    #         proof = self.proof_of_work(new_block)
    #         self.add_block(new_block, proof)
    #         self.unconfirmed_transactions = []
    #         return new_block.index

#    @property
#    def last_block(self):
#

blockchain = Blockchain()
        
@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)

    return json.dumps({"length": len(chain_data), "chain": chain_data})

@app.route('/') 
def test_message(): 
   return '<h1>Sup1</h1>'

if __name__ == "__main__": 
   app.run(debug=True, host='0.0.0.0', port=8000)

def display_transaction(transaction):
    for transaction in transactions:
        dict = transaction.to_dict()
        print ("sender: " + dict['sender'])
        print ('-----')
        print ("recipient: " + dict['recipient'])
        print ('-----')
        print ("value: " + str(dict['value']))
        print ('-----')
        print ("time: " + str(dict['time']))
        print ('-----')
        print ('--------------')


charles = User()
print(charles.identity)
jack = User()
print(jack.identity)

t = Transaction(
    charles,
    jack.identity,
    5.0
)
signature = t.sign_transaction()
print(signature)

transactions.append(t)

display_transaction(t)