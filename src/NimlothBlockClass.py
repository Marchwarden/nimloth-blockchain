from dataclasses import dataclass, field
import json

from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA

@dataclass
class NimlothBlock:
    previous_block_hash: str
    timestamp: float
    nonce: int = 0 
    verified_transactions_list: list = field(default_factory=list)

    def compute_hash(self) -> str:
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return SHA.new(block_string.encode()).hexdigest()