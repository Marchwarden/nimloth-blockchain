from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15

import requests

from ..block_files.block import NimlothBlock
from ..block_files.blockchain import Blockchain


class PeerNode:
    def __init__(self, ip_address: str, port: int):
        self.base_url = f"http://{ip_address}:{port}/"

    def send(self, transaction: dict) -> requests.Response:
        url = f"{self.base_url}transactions"
        req_return = requests.post(url, json=transaction)
        req_return.raise_for_status()
        return req_return


class Node:
    def __init__(self, blockchain: Blockchain):
        self.blockchain = blockchain
        self.transaction_data = {}

    def update_blockchain(self, blockchain: NimlothBlock):
        self.blockchain = blockchain

    def recieve(self, transaction: dict):
        self.transaction_data = transaction

    def broadcast(self):
        # fill node_list with PeerNodes
        node_list = []
        for node in node_list:
            try:
                node.send(self.transaction_data)
            except requests.ConnectionError:
                pass

    def validate_funds(self, sender_address: bytes, amount: int) -> bool:
        sender_balance = 0
        blockchain_chain = self.blockchain.chain
        for current_block in blockchain_chain:
            for transaction in current_block.verified_transactions_list:
                for input in transaction.inputs:
                    if transaction.sender.adress == sender_address:
                        sender_balance = sender_balance - input.transaction_data.value
                for output in transaction.outputs:
                    if output.public_key_hash == sender_address:
                        sender_balance = sender_balance + output.amount
        return amount <= sender_balance

    @staticmethod
    def validate_signature(
        public_key: bytes, signature: bytes, transaction_data: bytes
    ):
        public_key_object = RSA.import_key(public_key)
        transaction_hash = SHA256.new(transaction_data)
        pkcs1_15.new(public_key_object).verify(transaction_hash, signature)
