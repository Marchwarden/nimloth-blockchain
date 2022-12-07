from dataclasses import dataclass, field
import json

from Crypto.PublicKey import RSA  # pylint: disable=import-error
from Crypto.Random import get_random_bytes  # pylint: disable=import-error
from Crypto.Signature import pkcs1_15  # pylint: disable=import-error
from Crypto.Hash import SHA  # pylint: disable=import-error
from .transaction_tree import Node

# thing to add, pointers to abitrary next block and pointers to previous block
# possible imuttability imporvement add transaction hash AKA take current transaction and previous hash to create new hash which is used within block hash,
@dataclass
class NimlothBlock:
    previous_block_hash: str
    transaction_node: Node
    timestamp: float
    nonce: int = 0
    verified_transactions_list: list = field(default_factory=list)

    def compute_hash(self) -> str:
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return SHA.new(block_string.encode()).hexdigest()
