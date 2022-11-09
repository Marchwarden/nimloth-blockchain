from dataclasses import dataclass, field
import binascii
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA

@dataclass
class User:
    def __init__(self):
        self._private_key = RSA.generate(1024)
        self._public_key = self._private_key.publickey()
        self._signer = pkcs1_15.new(self._private_key)

    @property
    def identity(self):
        return binascii.hexlify(self._public_key.exportKey(format='DER')).decode('ascii')
