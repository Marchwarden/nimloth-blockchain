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
    hash: str
    previous_block_hash: str
    timestamp: float
    nonce: int = 0
    verified_transactions_list: list = field(default_factory=list)

    def compute_hash(self) -> str:
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return SHA.new(block_string.encode()).hexdigest()

    def clearblock(self):
        self.previous_block_hash = self.hash
        self.hash = "null"
        self.timestamp = 0
        self.nonce = 0
        self.verified_transactions_list = []
