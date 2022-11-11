import time as _time
from dataclasses import dataclass
import binascii
import collections

from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA

@dataclass
class Transaction:
    sender: str
    recipient: str 
    value: float 
    time: float = _time.time() 

    # TODO: what is the identity property?
    def to_dict(self) -> collections.OrderedDict:
        if self.sender == "Genesis":
            identity = "Genesis"
        else:
            identity = self.sender.identity
        
        return collections.OrderedDict({
            'sender': identity,
            'recipient': self.recipient,
            'value': self.value,
            'time': self.time })

    def sign_transaction(self) -> str:
        private_key = self.sender._private_key
        signer = pkcs1_15.new(private_key)
        h = SHA.new(str(self.to_dict()).encode('utf8')) # change var name
        
        return binascii.hexlify(signer.sign(h)).decode('ascii') 