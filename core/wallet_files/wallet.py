from dataclasses import dataclass, field
import binascii
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA

# TODO: are these attributes meant to be immutable?


@dataclass
class Coin:
    def __init__(self):
        self.name: str
        self.amount = 0

    def change_value(self, amount):
        if (self.amount + amount) < 0:
            return ValueError
        else:
            self.amount += amount


# pylint: disable-all
class Wallet:
    # _private_key: RSA.RsaKey = RSA.generate(1024)
    # _public_key: RSA.RsaKey = _private_key.publickey()
    # _signer: pkcs1_15.PKCS115_SigScheme = pkcs1_15.new(_private_key)
    # multi layer encryption
    # dependant on account information different encryption systems are used, and then account recovery questions are used as keywords for further private generation
    def __init__(self):
        self.owner_public: str
        self.coins = []

    def new_coin(self, name, amount):
        _coin = Coin(name)
        if amount != 0:
            _coin.change_value(amount)
        return self.coins.append(_coin)

    def search_for_coin(self, coin_name):
        for index, coin in enumerate(self.coins):
            if coin.name == coin_name:
                return index

    @property
    def identity(self) -> str:
        return binascii.hexlify(self._public_key.exportKey(format="DER")).decode(
            "ascii"
        )

    # add authorization and authentification
    # I.E. proof of stake, proof of access to resourses, proof of authroization of transaction
