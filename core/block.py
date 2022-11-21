from dataclasses import dataclass, field
import json
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA

# TODO: pointers to abitrary next block and pointers to previous block
# TODO: possible immutability improvement: add transaction hash AKA take current transaction and previous hash to create new hash which is used within block hash


@dataclass(frozen=True)
class NimlothBlock:
    """
    Block class
    """

    previous_block_hash: str
    timestamp: float
    nonce: int = 0
    hash: str = field(init=False)
    verified_transactions_list: list = field(default_factory=list)

    def __post_init__(self) -> None:
        """
        Generates and sets hash for block upon initialization
        """
        block_string = json.dumps(self.__dict__, sort_keys=True)
        hash_string = SHA.new(block_string.encode()).hexdigest()
        super().__setattr__("hash", hash_string)

        print(hash_string)
