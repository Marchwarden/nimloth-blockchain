from dataclasses import dataclass, field
import json

from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA

# thing to add, pointers to abitrary next block and pointers to previous block
# possible imuttability imporvement add transaction hash AKA take current transaction and previous hash to create new hash which is used within block hash,

@dataclass
class NimlothBlock:
    """This is the basic blockchain block class, it takes new transactions, and sets up the block data which is sent from a node to the blockchain
    attributes:
        index-int: this is the id number for the block, its used to make sure you are working on the correct block/lets you know if you need to rehash your block in the case that a new block is added to chain during block creation
        hash-str: the hashed identifier for this block, this uses the previous block hash, and all current transaction data to created an encrypted identifier for a block
        previous_block_hash-str:the stored block identifier for previous block hash
        timestamp-float: the time of creation of current block
        nonce-int: an arbitray value of zeros used to create a difficulty for decoding block hash, used as a security measure to prevent fraudulant blocks
        verified_transactions_list-list:basic empty python list used to store all transactions
    Returns:
        _type_: _description_
    """
    index: int
    hash: str
    previous_block_hash: str
    timestamp: float
    nonce: int = 0
    verified_transactions_list: list = field(default_factory=list)

    #takes all of current blocks data, turns it into json text then encodes it to create a new block
    def compute_hash(self) -> str:
        block_string = json.dumps(self.to_dict(), sort_keys=True)
        return SHA.new(block_string.encode()).hexdigest()

    #erases all data from current block, this should be removed, and nimlothblock class should be reconfigured to be a block factory tbd
    def clearblock(self):
        self.previous_block_hash = self.hash
        self.hash = "null"
        self.timestamp = 0
        self.nonce = 0
        self.verified_transactions_list = []

    #returns all block data organized into a dictonary format, primarily used to take dictonary format and turn it into json format
    def to_dict(self):
        block_data = {
            "index": self.index,
            "hash": self.hash,
            "previous_hash": self.previous_block_hash,
            "timestamp": self.timestamp,
            "nonce": self.nonce,
            "transactions": self.verified_transactions_list,
        }
        return block_data
    
    #returns all blockdata organized in a json fromat, by first getting the dictionary format, and then dumping all values
    def to_json(self):
        return json.dumps(self.to_dict)
