import time as _time
from dataclasses import dataclass
import binascii
import collections

from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA

import coinList
import networkList

@dataclass
class Transaction:
    sender: any  # TODO: Change
    recipient: str
    value: float
    coin_type: str  # Need to implement control and security protocols to check b4 compiled into blocks.
    network: str
    time: float = _time.time()
    # add cointype, blockgroup, ether chain information, other arbitrary info

    # TODO: what is the identity property?
    def to_dict(self) -> collections.OrderedDict:
        if self.sender == "Genesis":
            identity = "Genesis"
        else:
            identity = self.sender.identity

        return collections.OrderedDict(
            {
                "sender": identity,
                "recipient": self.recipient,
                "value": self.value,
                "time": self.time,
                "coinType": self.coin_type,
                "network": self.network
            }
        )

    def display_transaction(self, transactions):
        for transaction in transactions:
            dict = transaction.to_dict()
            print("sender: " + dict["sender"])
            print("-----")
            print("recipient: " + dict["recipient"])
            print("-----")
            print("value: " + str(dict["value"]))
            print("-----")
            print("time: " + str(dict["time"]))
            print("-----")
            print("--------------")

    # TODO: this should not work
    def sign_transaction(self) -> str:
        private_key = self.sender._private_key
        signer = pkcs1_15.new(private_key)
        hash = SHA.new(str(self.to_dict()).encode("utf8"))  # change var name

        return binascii.hexlify(signer.sign(hash)).decode("ascii")

#basic idea of system to check if the transaction is possible before initial creation by user.
#prevents customers from sending money into the void by accident.

    def validate_coinType(self: str) -> bool:   
        if self.coin_type in coinList:
            coin_type_valid == True
        else:
            coin_type_valid == False
        return(coin_type_valid)

    def validate_network(self: str) -> bool:   
        if self.network in networkList:
            network_valid == True
        else:
            network_valid == False
        return(network_valid)

    def parameters_valid(self: str) -> bool:
        if coin_type_valid and network_valid == True:
            transactionParameters == True
        else:
            transactionParameters == False
        return(transactionParameters)
            