from dataclasses import dataclass, field
import binascii
from ..transaction_files.transaction import Transaction
from .wallet import UserWallet, Coin
from ..node_files.node import Node
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA

# pylint: disable-all
# TODO: are these attributes meant to be immutable?
import requests


class UserNode:
    """Usernode: this is the class which sets up the node object that the user interacts with and allows the sending of transactions between nodes
    """
    def __init__(self):
        self.ip = "127.0.0.1"
        self.port = 5000
        self.base_url = f"http://{self.ip}:{self.port}/"

    def send(self, transaction: dict) -> requests.Response:
        url = f"{self.base_url}transactions"
        req_return = requests.post(url, json=transaction)
        req_return.raise_for_status()
        return req_return


class User:
    # _private_key: RSA.RsaKey = RSA.generate(1024)
    # _public_key: RSA.RsaKey = _private_key.publickey()
    # _signer: pkcs1_15.PKCS115_SigScheme = pkcs1_15.new(_private_key)
    # multi layer encryption
    # dependant on account information different encryption systems are used, and then account recovery questions are used as keywords for further private generation
    """User: this is the user data class, it contains a users wallet object
        Attributes:
        private_key-bytes: this is the users private key
        public_key-bytes: this is the users public key
        wallet-Wallet: this is the user wallet object, based on the users public key
        node: a node object from node.py
    """
    def __init__(self):
        self.private_key = self.generate_private_key()
        self.public_key = self.generate_public_key(self.private_key)
        # self.wallets = self.generate_wallets()
        self.wallet = self.generate_wallet()
        self.node = UserNode()

    @property
    def identity(self) -> str:
        return binascii.hexlify(self._public_key.exportKey(format="DER")).decode(
            "ascii"
        )

    #given a privatekey value as a str, sets the private and public key for user
    def set_keys(self, private):
        self.private_key = RSA.importKey(private)
        self.public_key = self.generate_public_key(self.private_key)

    # generates given user wallet, change this in future to first check for existing wallet
    def generate_wallet(self):
        self.wallet= UserWallet(self.private_key)
    
    # adds new coin subwallet to users list of wallets
    def add_new_coin_wallet(self, cointype, amount=0, onchain, multisig, mnemonic):
        self.wallet.generate_new_coin_wallet(cointype,amount, onchain, multisig, mnemonic)
    #generates a RSA private key
    def generate_private_key(self):
        privatekey = RSA.generate(2048)
        return privatekey

    #generates a RSA public key
    def generate_public_key(self, private_key):
        publickey = self.private_key.publickey().export_key()
        return publickey

    # this is currently inefficient and pointless, but will be important for taking data as bytes, or json blocks rather than just individual fields
    def generate_transaction(self, recipient, coin, value):
        print(recipient)
        print(coin)
        transaction = Transaction(self.wallet, recipient, value, coin)
        return self.create_transaction(transaction)

    #this checks to make sure all users in a transaction have the correct amount of currency in thier wallets, then signs and send transaction to useres node object
    def create_transaction(self, transaction_data: Transaction):
        # if self.check_transaction(transaction_data) != True:
        #     return ValueError
        # new_transaction = Transaction(
        #     self.public_key,
        #     transaction_data.recipient,
        #     transaction_data.value,
        #     transaction_data.coin,
        #  n)
        new_transaction = self.sign_transaction(transaction_data)
        # self.node.send({"transaction": new_transaction.to__dict()})
        return new_transaction

    #Checks to make sure user has the correct amount of currency in thier wallet before a transaction
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

    #signs a transaction as a wallet
    def sign_transaction(self, transaction: Transaction):
        transaction.sign_transaction(self.private_key)
        return transaction

    # obsolete signing method
    # def sign_transaction(self, transaction, private_key):
    #     sha256 = ecdsa.sha256
    #     secp256k1 = curve.secp256k1
    #     signature = ecdsa.sign(transaction, private_key, secp256k1, sha256)
    #     return signature

    # add authorization and authentification
    # I.E. proof of stake, proof of access to resourses, proof of authroization of transaction
