import hashlib
import json
import time

class NimlothCoinBlock:
    def __init__(self, previous_block_hash, transaction_list, timestamp, nonce=0):
        self.previous_block_hash = previous_block_hash
        self.transactions_list = transaction_list
        self.timestamp = timestamp
        self.nonce = nonce

    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()


class Blockchain:
    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = NimlothCoinBlock(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    diffiiculty = 2
    def proof_of_work(self, block):
        block.nonce = 
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
        return (block_hash.startswith('0'*Blockchain.diffiiculty) and 
                block_hash == block.compute_hash())
    
    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    def mine(self):
            if not self.unconfirmed_transactions:
                return False
            
            last_block = self.last_block

            new_block = Block(index = last_block.index + 1,
                              transactions = self.unconfirmed_transactions,
                              timestamp = time.time(),
                              previous_hash=last_block.hash)

            proof = self.proof_of_work(new_block)
            self.add_block(new_block, proof)
            self.unconfirmed_transactions = []
            return new_block.index


