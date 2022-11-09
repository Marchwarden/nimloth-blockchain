from dataclasses import dataclass, field
import binascii
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA

@dataclass
class User:
    _private_key = RSA.generate(1024)
    _public_key = _private_key.publickey()
    _signer = pkcs1_15.new(_private_key)

    @property
    def identity(self):
        return binascii.hexlify(self._public_key.exportKey(format='DER')).decode('ascii')
