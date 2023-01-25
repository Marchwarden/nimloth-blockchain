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
    def __init__(self):
        recipient: str
        coin: str
        value: str


# neccessary class should be expanded upon
@dataclass
class TransactionInput:
    transaction_data: TransactionData
    output_index: int
    transaction_hash: str
    public_key: bytes
    signature: bytes = None

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
    amount: int
    coin_type: str
    public_key_hash: str


@dataclass
class TransactionNew:
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
#
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
