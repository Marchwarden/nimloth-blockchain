import time as _time

import binascii
import collections
import json
from dataclasses import dataclass
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA, SHA256

from ..wallet_files.wallet import Wallet

# unneccessary class - should be removed
@dataclass
class TransactionData:
    #a basic dataclass for holding data from a transaction
    #holds a recipient:str-which is the address of the recipient
    #coin:str -the name of the coin sent
    #value:str a str represent the amount of a coin spent
    def __init__(self):
        recipient: str
        coin: str
        value: str


# neccessary class should be expanded upon
@dataclass
class TransactionInput:
    """This is the class generator for a transactions inputs
    Attributes:
    transaction_data:-data containing the recipient, coin, and value all in string format
    output_index: an integer to refrence what transaction outputs were used to create this transaction input
    transaction_hash:hashed string of current transaction
    publick_key: a byte object refrencing the public key of the person creating the transaction
    signature: the signature of the person who created the transaction
    Returns:
        _type_: _description_
    """
    transaction_data: TransactionData
    output_index: int
    transaction_hash: str
    public_key: bytes
    signature: bytes = None

    #returns a jsonified version of all data in the transaction inputs
    def _to_json(self) -> str:
        if self.signature is None:
            return json.dumps(
                {
                    "transaction_data": self.transaction_data,
                    "output_index": self.output_index,
                    "transaction_hash": self.transaction_hash,
                }
            )
        return json.dumps(
            {
                "transaction_data": self.transaction_data,
                "output_index": self.output_index,
                "transaction_hash": self.transaction_hash,
                "public_key": self.public_key,
                "signature": self.signature,
            }
        )


@dataclass
class TransactionOutput:
    #a basic dataclass for holding data from a transactionoutput
    #amount:int - an int showing how much of the coin is outputted
    #cointype:str -the type of coin used in this transaction
    #the public key of the reciever of the transaction
    amount: int
    coin_type: str
    public_key_hash: str


@dataclass
class TransactionNew:
    """TransactionNew: this is the transaction class which holds the inputs and outputs of a transaction, this is what is passed to the blockchain transaction
    Attributes:
        Sender: a Wallet object of the person sending the transaction
        Inputs: a list of transaction inputs which are needed for this transaction
        Outputs: a list of all transaction outputs created by this transaction
        Time: time of transaction
    Returns:
        _type_: _description_
    """
    sender: Wallet  # this is now the wallet address(could possibly change to wallet object)
    inputs: list[TransactionInput]
    outputs: list[TransactionOutput]
    time: float = _time.time()

    # TODO: what is the identity property?
    def _to_dict(self) -> collections.OrderedDict:
        return collections.OrderedDict(
            {
                "sender": str(self.sender.address),
                "inputs": [
                    transaction_input._to_json() for transaction_input in self.inputs
                ],
                "outputs": [
                    transaction_output._to_json() for transaction_output in self.outputs
                ],
                "time": str(self.time),
            }
        )

    def to__dict(self):
        return self._to_dict()

    def to_bytes(self):
        transaction_byte_data = self.to__dict()
        return json.dumps(transaction_byte_data, indent=2).encode("utf-8")

    # # TODO: this is an old transaction signing
    # TODO fix sign transaction to represent addreses rather than public keys
    #uses senders private key to sign and verify a transaction
    def sign_transaction(self, privatekey) -> str:
        transaction_data = self.to_bytes()
        signer = pkcs1_15.new(privatekey)
        hash = SHA256.new(transaction_data)  # change var name
        signature = signer.sign(hash)
        input_signature = binascii.hexlify(signature).decode("utf-8")
        for transaction_input in self.inputs:
            transaction_input.signature = input_signature
            transaction_input.public_key = self.sender.owner_public


#
#
#
#
#old transaction class
@dataclass
class Transaction:
    sender: Wallet  # this is now the wallet address(could possibly change to wallet object)
    recipient: str
    value: float
    coin_type: str  # Need to implement control and security protocols to check b4 compiled into blocks.
    time: float = _time.time()
    signature = None
    # add cointype, blockgroup, ether chain information, other arbitrary info

    # TODO: what is the identity property?
    def _to_dict(self) -> collections.OrderedDict:
        if self.sender == "Genesis":
            identity = "Genesis"
        else:
            identity = self.sender.address

        return collections.OrderedDict(
            {
                "sender": str(identity),
                "recipient": str(self.recipient),
                "value": str(self.value),
                "time": str(self.time),
                "coinType": self.coin_type,
            }
        )

    def to__dict(self):
        return self._to_dict()

    def to_bytes(self):
        transaction_byte_data = self.to__dict()
        return json.dumps(transaction_byte_data, indent=2).encode("utf-8")

    def display_transaction(self, transactions):
        for transaction in transactions:
            dict = transaction._to_dict()
            print("sender: " + dict["sender"])
            print("-----")
            print("recipient: " + dict["recipient"])
            print("-----")
            print("value: " + str(dict["value"]))
            print("-----")
            print("time: " + str(dict["time"]))
            print("-----")
            print("--------------")

    # # TODO: this is an old transaction signing
    # TODO fix sign transaction to represent addreses rather than public keys
    def sign_transaction(self, privatekey) -> str:
        transaction_data = self.to_bytes()
        signer = pkcs1_15.new(privatekey)
        hash = SHA256.new(transaction_data)  # change var name
        signature = signer.sign(hash)
        self.signature = binascii.hexlify(signature).decode("utf-8")

##multicoin transaction have it be a set of two transactions, all succeed or all fail, one transaction is one user takes outputs and puts them in admin coin wallet, the  sadmin wallet account the  intiates a secondary transaction taking stored outputs and sending them to original user, transactions are then put on a merkle tree and oublished to block