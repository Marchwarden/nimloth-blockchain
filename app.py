from flask import Flask
from dataclasses import dataclass, field
import hashlib
import json
import datetime

import rsa, binascii


import numpy as np
import pandas as pd
import logging
import collections


app = Flask(__name__)

@dataclass
class NimlothCoinBlock:
    previous_block_hash: str
    timestamp: str
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
        genesis_block = NimlothCoinBlock(0, [], datetime.time(), "0")
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

    @property
    def last_block(self):
        return self.chain[-1]

blockchain = Blockchain()
        
@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)

    return json.dumps({"length": len(chain_data), "chain": chain_data})

@app.route('/') 
def test_message(): 
    return 'Hello!'

if __name__ == "__main__": 
    app.run(debug=True, host='0.0.0.0')

@dataclass
class Client:
    def __init__(self):
        random = hashlib.Random.new().read
        self._private_key = rsa.generate(1024, random)
        self._public_key = self._private_key.publickey()
        self._signer = hashlib.new(self._private_key)
    @property
    def identify(self):
        return
binascii.hexlify(self._public_key.exportKey(format='DER')).decode('ascii')
