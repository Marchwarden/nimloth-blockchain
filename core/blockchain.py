import time
from urllib import request
import urllib.parse

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
        previous_hash = block.previous_block_hash  # self.last_block.hash
        if previous_hash != block.previous_block_hash:
            return False
        if self.is_valid_proof(block, proof):
            block.verified_transactions_list = []
            return False
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
        self.unconfirmed_transactions.append(transaction)

    def printhash(self) -> str:
        latestblock = self.chain[len(self.chain) - 1]
        return latestblock.hash

    # add overall blockchain check(\)
    # add variable nonce value
    # add node registration
    # conflict resolution
    # payment verification full and simple implementation
