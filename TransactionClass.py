import time
from dataclasses import dataclass, field
import binascii
import collections

from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA

@dataclass
class Transaction:
    def __init__(self, sender, recipient, value):
        self.sender = sender
        self.recipient = recipient
        self.value = value
        self.time = time.time()

    def to_dict(self):
        if self.sender == "Genesis":
            identity = "Genesis"
        else:
            identity = self.sender.identity
        
        return collections.OrderedDict({
            'sender': identity,
            'recipient': self.recipient,
            'value': self.value,
            'time': self.time })

    def sign_transaction(self):
        private_key = self.sender._private_key
        signer = pkcs1_15.new(private_key)
        h = SHA.new(str(self.to_dict()).encode('utf8'))
        
        return binascii.hexlify(signer.sign(h)).decode('ascii') 