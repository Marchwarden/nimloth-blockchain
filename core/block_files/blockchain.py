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
    """Blockchain: the basic empty blockchain generation class
        -This class is to be instantiated, and then filled by node upon loading

    Attributes
    unconfirmed_transactions:list- holds a list of all transactions not currently put into a block
    chain: list[NimlothBlock]- a list of nimlothblocks, representing all confirmed blocks on the blockchain
    difficulty:int - an in representing the current difficulty value for the next block that is created
    nodes: these are the instances of access points to the main chain, this is where vereified data is passed to the chain when updating blocks, or from the chain to the node when updating the entire chain
    Returns:
        _type_: _description_
    """
    unconfirmed_transactions: list = field(default_factory=list)
    chain: list[NimlothBlock] = field(default_factory=list)
    difficulty: int = 2
    nodes = set()

    #this sets up the first block of the blockchain before it is filled
    def __post_init__(self):
        self.create_genesis_block()

    # initialization of chain for blockchain, sets the first block as empty, with a 0 index, no nonce, and no transactions, then it assigns an arbitrary hash and adds it to current chain
    # TODO: hash is not a property of block
    def create_genesis_block(self) -> None:
        genesis_block = NimlothBlock(
            0, "null", "0", time.time(), 0, []
        )  # change argument order

        genesis_block.hash = genesis_block.compute_hash()

        self.chain.append(genesis_block)

    #sets registered terminal url, as current node url, creating a new node attached to blockchain at users current address
    #arguments: address- a string with a value following a basic url structure
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
    #checks to make sure block has correct hashed value given the transactions and nonce 
    #arguments-  block:NimlothBlock- this is the current block that you are trying to verify and add to the chain
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

    #calculates next nonce value for a block given the current difficulty of the blockchain
    #arguments-  block:NimlothBlock- this is the current block that you are trying to verify and add to the chain
    def get_nonce(self, new_block: NimlothBlock) -> int:
        new_block_hash = new_block.hash
        nonce = new_block.nonce
        starting_zeros = "".join([str(0) for _ in range(self.difficulty)])
        while not new_block_hash.startswith("0" * Blockchain.difficulty):
            nonce += 1
            new_block.nonce = nonce
            new_block_hash = new_block.compute_hash()
        return nonce

    #creates a new block and fills it with all currently unconfirmed transactions on the blockchain
    #then gives the new block a calculated nonce, and hash value and tries to validate it
    #returns the newblock information if block is valid and added to chain returns false otherwise(should switch to throwing error)
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

    #Checks to make sure that the newley created block has the correct nonce value given blockchain difficulty
    #returns AssertionError if validation fails, and true if validation succeds
     #arguments-  block:NimlothBlock- this is the current block that you are trying to verify and add to the chain
    def validate_block(self, new_block: NimlothBlock):
        new_hash = new_block.hash
        number_of_zeros_string = "".join([str(0) for _ in range(self.difficulty)])
        try:
            assert new_hash.startswith(number_of_zeros_string)
            return True
        except AssertionError:
            print("Proof of work validation failed")
            return False

    #will check user transaction values against externally stored wallet amounts, not yet implemented
    def validate_transaction(self, new_block: NimlothBlock):
        for transaction in new_block.verified_transactions_list:
            continue
            # todo: write aws server fund checking:
        return True

    # TODO: type proof parameter
    # TODO: hash is not a property of block
    # possibly have it return the block rather than a bool
    #Checks a block via the is_valid_proof method, returning false and deleting all transactions if not valid
    #if valid, it adds current block to blockchain and clears all uncofirmed transactions for blockchain object
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
    #checks a supposed block_hash against blockchain difficulty and against recomputed hash to make sure they are the same
    #should throw error if returns false
    def is_valid_proof(self, block: NimlothBlock, block_hash) -> bool:
        return (
            block_hash.startswith("0" * Blockchain.difficulty)
            and block_hash == block.compute_hash()
        )

    #Turns transaction object into an organized dictionary and then adds dictionary to list of unconfirmed transactions in blockchain
    # TODO: type transaction parameter
    def add_new_transaction(self, transaction) -> None:
        transaction_dict = transaction.to__dict()
        self.unconfirmed_transactions.append(transaction_dict)

    # getter functions
    #returns the latest block object in chain
    def get_latest_block(self) -> NimlothBlock:
        latestblock = self.chain[len(self.chain) - 1]
        return latestblock

    #returns the hash of the latest block object in chain
    def get_previous_hash(self) -> str:
        lastblock = self.get_latest_block()
        return lastblock.hash

    #returns indec of latest block object in chain
    def get_current_index(self) -> int:
        lastblock = self.get_latest_block()
        lastindex = lastblock.index
        return lastindex + 1

    #returns entire blockchain in a dictonary format so it can be turned into a json format
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

    #returns jsonified version of blockchain data
    def _to_json(self):
        # pylint: disable =no-member
        return self.to_json()
        # pylint: enable=no-member

    #sets current blockchain object, equal to inputted blockchain object
    def load(self, blockchain):
        self.unconfirmed_transactions = blockchain.unconfirmed_transactions
        self.difficulty = blockchain.difficulty
        self.chain = blockchain.chain

    # add overall blockchain check(\)
    # add variable nonce value
    # add node registration
    # conflict resolution
    # payment verification full and simple implementation
