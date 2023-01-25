import time
import json
from urllib import request
import urllib.parse


from dataclasses import dataclass, field
from dataclasses_json import dataclass_json

from .block import NimlothBlock


@dataclass_json
@dataclass
class Blockchain:
    unconfirmed_transactions: list = field(default_factory=list)
    chain: list[NimlothBlock] = field(default_factory=list)
    difficulty: int = 2
    nodes = set()

    def __post_init__(self):
        self.create_genesis_block()

    # initialization of chain for blockchain
    # TODO: hash is not a property of block
    def create_genesis_block(self) -> None:
        genesis_block = NimlothBlock(
            0, "null", "0", time.time(), 0, []
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

    # old proof_of_work, currently not working
    def proof_of_work(self, block: NimlothBlock) -> str:
        block.nonce = 0
        block.verified_transactions_list = self.unconfirmed_transactions
        computed_hash = block.compute_hash()
        while not computed_hash.startswith("0" * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    # TODO:add new block creation and new proof of work
    def proof_of_work_dev(self):
        return None

    def get_nonce(self, new_block: NimlothBlock) -> int:
        new_block_hash = new_block.hash
        nonce = new_block.nonce
        starting_zeros = "".join([str(0) for _ in range(self.difficulty)])
        while not new_block_hash.startswith("0" * Blockchain.difficulty):
            nonce += 1
            new_block.nonce = nonce
            new_block_hash = new_block.compute_hash()
        return nonce

    def create_block(self):
        new_block = NimlothBlock(
            self.get_current_index(),
            "",
            self.get_previous_hash(),
            time.time(),
            0,
            self.unconfirmed_transactions,
        )
        new_block.nonce = self.get_nonce(new_block)
        new_block.hash = new_block.compute_hash()
        if self.validate_block(new_block):
            self.unconfirmed_transactions = []
            self.chain.append(new_block)
            return new_block
        return False

    def validate_block(self, new_block: NimlothBlock):
        new_hash = new_block.hash
        number_of_zeros_string = "".join([str(0) for _ in range(self.difficulty)])
        try:
            assert new_hash.startswith(number_of_zeros_string)
            return True
        except AssertionError:
            print("Proof of work validation failed")
            return False

    def validate_transaction(self, new_block: NimlothBlock):
        for transaction in new_block.verified_transactions_list:
            continue
            # todo: write aws server fund checking:
        return True

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

    # this is for development testing purposes only
    def add_block_dev(self, new_hash):

        genesis_block2 = NimlothBlock(
            self.get_current_index(),
            new_hash,
            self.get_previous_hash(),
            time.time(),
            0,
            self.unconfirmed_transactions,
        )
        self.unconfirmed_transactions = []
        genesis_block2.hash = genesis_block2.compute_hash()
        self.chain.append(genesis_block2)

    # TODO: type block_hash parameter
    def is_valid_proof(self, block: NimlothBlock, block_hash) -> bool:
        return (
            block_hash.startswith("0" * Blockchain.difficulty)
            and block_hash == block.compute_hash()
        )

    # TODO: type transaction parameter
    def add_new_transaction(self, transaction) -> None:
        transaction_dict = transaction.to__dict()
        self.unconfirmed_transactions.append(transaction_dict)

    # getter functions
    def get_latest_block(self) -> NimlothBlock:
        latestblock = self.chain[len(self.chain) - 1]
        return latestblock

    def get_previous_hash(self) -> str:
        lastblock = self.get_latest_block()
        return lastblock.hash

    def get_current_index(self) -> int:
        lastblock = self.get_latest_block()
        lastindex = lastblock.index
        return lastindex + 1

    @property
    def to_dict(self):
        block_list = []
        transaction_list = []
        for transaction in self.unconfirmed_transactions:
            transaction_list.append(transaction.to_dict())
        current_block = self.chain[len(self.chain) - 1]
        for block in self.chain:
            block_list.append(block.to_dict())
        blockchaindict = {"dictionary": block_list}
        return block_list

    def _to_json(self):
        # pylint: disable =no-member
        return self.to_json()
        # pylint: enable=no-member

    def load(self, blockchain):
        self.unconfirmed_transactions = blockchain.unconfirmed_transactions
        self.difficulty = blockchain.difficulty
        self.chain = blockchain.chain

    # add overall blockchain check(\)
    # add variable nonce value
    # add node registration
    # conflict resolution
    # payment verification full and simple implementation
