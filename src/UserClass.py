from dataclasses import dataclass, field
import binascii
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA

# TODO: are these attributes meant to be immutable?

class User:
    # _private_key: RSA.RsaKey = RSA.generate(1024)
    # _public_key: RSA.RsaKey = _private_key.publickey()
    # _signer: pkcs1_15.PKCS115_SigScheme = pkcs1_15.new(_private_key)
    
    def __init__(self):
        self._private_key = RSA.generate(1024)
        self._public_key = self._private_key.publickey()
        self._signer = pkcs1_15.new(self._private_key)

    @property
    def identity(self) -> str:
        return binascii.hexlify(self._public_key.exportKey(format='DER')).decode('ascii')
    #add authorization and authentification
    #I.E. proof of stake, proof of access to resourses, proof of authroization of transaction