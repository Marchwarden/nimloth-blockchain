from dataclasses import dataclass, field
import binascii
from ..transaction_files.transaction import Transaction
from .wallet import Wallet, Coin
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA

# pylint: disable-all
# TODO: are these attributes meant to be immutable?


class User:
    # _private_key: RSA.RsaKey = RSA.generate(1024)
    # _public_key: RSA.RsaKey = _private_key.publickey()
    # _signer: pkcs1_15.PKCS115_SigScheme = pkcs1_15.new(_private_key)
    # multi layer encryption
    # dependant on account information different encryption systems are used, and then account recovery questions are used as keywords for further private generation
    def __init__(self):
        self.private_key = self.generate_private_key()
        self.public_key = self.generate_public_key(self.private_key)
        self.wallet = Wallet(self.public_key)

    @property
    def identity(self) -> str:
        return binascii.hexlify(self._public_key.exportKey(format="DER")).decode(
            "ascii"
        )

    def generate_private_key(self):
        privatekey = RSA.generate(2048)
        return privatekey

    def generate_public_key(self, private_key):
        publickey = self.private_key.publickey().export_key()
        return publickey

    # this is currently inefficient and pointless, but will be important for taking data as bytes, or json blocks rather than just individual fields
    def generate_transaction(self, recipient, coin, value):
        transaction = Transaction(self.wallet, recipient, value, coin)
        return self.create_transaction(transaction)

    def create_transaction(self, transaction_data: Transaction):
        # if self.check_transaction(transaction_data) != True:
        #     return ValueError
        # new_transaction = Transaction(
        #     self.public_key,
        #     transaction_data.recipient,
        #     transaction_data.value,
        #     transaction_data.coin,
        # )
        new_transaction = self.sign_transaction(transaction_data)
        return new_transaction

    def check_transaction(self, transaction_data):
        if self.public_key != self.wallet.owner_public:
            return NameError
        if self.wallet.search_for_coin(transaction_data.coin_type) == -1:
            return ValueError
        else:
            if (
                self.wallet.coins[
                    self.wallet.search_for_coin(transaction_data.coin)
                ].value
                < transaction_data.value
            ):
                return ValueError
        return True
    
    def sign_transaction(self, transaction):
        transaction.sign_transaction(self.private_key)
        return transaction
    #obsolete signing method
    # def sign_transaction(self, transaction, private_key):
    #     sha256 = ecdsa.sha256
    #     secp256k1 = curve.secp256k1
    #     signature = ecdsa.sign(transaction, private_key, secp256k1, sha256)
    #     return signature

    # add authorization and authentification
    # I.E. proof of stake, proof of access to resourses, proof of authroization of transaction
