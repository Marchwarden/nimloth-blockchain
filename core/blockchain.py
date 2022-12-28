import time
from urllib import request
import urllib.parse
from flask_mysqldb import MySQL
from dataclasses import dataclass, field

from .block import NimlothBlock


@dataclass
class Blockchain:
    unconfirmed_transactions: list = field(default_factory=list)
    chain: list = field(default_factory=list)
    difficulty: int = 2
    nodes = set()

    def __post_init__(self):
        self.create_genesis_block()

    # initialization of chain for blockchain
    # TODO: hash is not a property of block
    def create_genesis_block(self) -> None:
        genesis_block = NimlothBlock(
            "null", "0", time.time(), 0, []
        )  # change argument order

        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)
        cur = MySQL.connection.cursor()
        cur.execute("INSERT INTO blockchain_chain(block, nonce, hash, prev_hash, timestamp, data) VALUES(%s, %s, %s, %s, %s, %s)",
        (genesis_block.index, genesis_block.nonce, genesis_block.hash, genesis_block.previous_block_hash, genesis_block.timestamp, genesis_block.verified_transactions_list))
        MySQL.connection.commit() 
        
    #need parrallel programming put in
    def register_node(self, address):
        passed_url = urllib.parse.urlparse(address)
        self.nodes.add(passed_url.netloc)

    # conflic resolution
    # TODO: this does not work
    def resolve_conflicts(self):

        neighbours = self.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            # response = request.get(f"http://{node}/chain")
            response = None
            if response.status_code == 200:
                length = response.json()["length"]
                chain = response.json()["chain"]

                # Check if the length is longer and the chain is valid
                if length > max_length:  # and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False

    def proof_of_work(self, block: NimlothBlock) -> str:
        block.nonce = 0
        block.verified_transactions_list = self.unconfirmed_transactions
        computed_hash = block.compute_hash()
        while not computed_hash.startswith("0" * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    # TODO: type proof parameter
    # TODO: hash is not a property of block
    # possibly have it return the block rather than a bool
    def add_block(self, block: NimlothBlock, proof) -> bool:
        cur = MySQL.connection.cursor()
        previous_hash = block.previous_block_hash  # self.last_block.hash
        if previous_hash != block.previous_block_hash:
            return False
        if self.is_valid_proof(block, proof):
            block.verified_transactions_list = []
            return False
        result = cur.execute("SELECT * FROM blockchain_chain")
        chain = cur.fetchall()
        current_index = len(chain) + 1
        if result > 0 :
            length = len(chain)
            cur.execute("SELECT * from blockchain_chain WHERE block=%s", [length])
            last_block = cur.fetchone()
            prev_hash = last_block['hash']
            block.hash = proof
            self.unconfirmed_transactions = []
            self.chain.append(block)
            self.unconfirmed_transactions.clear()
            return True

    # TODO: type block_hash parameter
    def is_valid_proof(self, block: NimlothBlock, block_hash) -> bool:
        return (
            block_hash.startswith("0" * Blockchain.difficulty)
            and block_hash == block.compute_hash()
        )

    # TODO: type transaction parameter
    def add_new_transaction(self, transaction) -> None:
        cur = MySQL.connection.cursor()
        result = cur.execute("SELECT * FROM blockchain_transactions")
        transactions = cur.fetchall()
        if result > 0:
            for transact in transactions:
                trans = json.loads(transact['transaction'])
                if trans['transaction_id'] == new_transaction['transaction_id']:
                    print('transaction {} already exists in the pool'.format(trans))
                    return
                self.unconfirmed_transactions.append(transaction)

    def printhash(self) -> str:
        latestblock = self.chain[len(self.chain) - 1]
        return latestblock.hash

    # add overall blockchain check(\)
    # add variable nonce value
    # add node registration
    # conflict resolution
    # payment verification full and simple implementation
