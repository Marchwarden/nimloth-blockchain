from dataclasses import dataclass, field
import json

from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA

Genesis_Data = {
    "previous_block_hash": "genesis_last_hash",
    "hash": "genesis_hash",
    "timestamp": 1,
    "nonce": "genesis_nonce",
    "verified_transaction_lists": [],
}

# thing to add, pointers to abitrary next block and pointers to previous block
# possible imuttability imporvement add transaction hash AKA take current transaction and previous hash to create new hash which is used within block hash,
@dataclass
class NimlothBlock:
    previous_block_hash: str
    hash: str
    timestamp: float
    nonce: int = 0
    verified_transactions_list: list = field(default_factory=list)

    def __init__(
        self, previous_block_hash, timestamp, nonce, verified_transaction_list
    ):
        self.previous_block_hash = previous_block_hash
        self.timestamp = timestamp
        self.nonce = nonce
        self.verified_transactions_list = verified_transaction_list

    def __repr__(self):
        return (
            "Block("
            f"previous_block_hash: {self.previous_block_hash},"
            f"hash: {self.hash}"
            f"timestamp: {self.timestamp}, "
            f"nonce: {self.nonce}, "
            f"verified_transaction_list: {self.verified_transactions_list}, "
        )

    def compute_hash(self) -> str:
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return SHA.new(block_string.encode()).hexdigest()
