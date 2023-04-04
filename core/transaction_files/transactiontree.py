import json
import time as _time
from dataclasses import dataclass
import binascii
import collections
import math

# type: ignore
from Crypto.PublicKey import RSA  # pylint: disable=import-error
from Crypto.Random import get_random_bytes  # pylint: disable=import-error
from Crypto.Signature import pkcs1_15  # pylint: disable=import-error
from Crypto.Hash import SHA  # pylint: disable=import-error
from .transaction import Transaction


class Node:
    """Node class-different from blockchain nodes, this just holds a value and two pointers to children
    """
    def __init__(self, value: str, left_child=None, right_child=None):
        self.value = value
        self.left_child = left_child
        self.right_child = right_child


class Transactiontree:
    """Transactiontree: this class holds an array of transaction in nodes
        Attributes:
        Merkle_hash: the hash for the trees entire transaction
        nodes: an array of node objects
        transactions: an array of transactions that will be stored in the transaction tree
        
    """
    def __init__(self, transactions):
        self.merkle_hash: str
        self.nodes = []
        self.transactions = []

    #uses all data in the tree to calulate the trees hash value
    def calculate_hash(self, data) -> str:
        transaction_string = json.dumps(data.__dict__, sort_keys=True)
        return SHA.new(transaction_string.encode()).hexdigest()

    #hashes an array of transactions, and adds them to the tree
    def hash_transactions(self, transactions):
        for i in transactions:
            self.transactions.append(self.calculate_hash(i))

    #computes the minimum possible depth of a tree with number_of_leaves nodes
    def compute_tree_depth(self, number_of_leaves: int) -> int:
        return math.ceil(math.log2(number_of_leaves))

    #computes wether or not the amount of nodes in a tree is a power of 2
    def is_power_of_2(self, number_of_leaves: int) -> bool:
        return math.log2(number_of_leaves).is_integer()

    #Creates empty nodes to fill tree if the amount of nodes is not a power of 2
    def fill_set(self, list_of_nodes: list):
        current_number_of_leaves = len(list_of_nodes)
        if self.is_power_of_2(current_number_of_leaves):
            return list_of_nodes
        total_number_of_leaves = 2 ** self.compute_tree_depth(current_number_of_leaves)
        if current_number_of_leaves % 2 == 0:
            for i in range(current_number_of_leaves, total_number_of_leaves, 2):
                list_of_nodes = list_of_nodes + [list_of_nodes[-2], list_of_nodes[-1]]
        else:
            for i in range(current_number_of_leaves, total_number_of_leaves):
                list_of_nodes.append(list_of_nodes[-1])
        return list_of_nodes

    #builds the transaction tree, filling nodes with transaction values
    def build_transaction_tree(self) -> Node:
        complete_set = self.fill_set(self.transactions)
        old_set_of_nodes = [Node(self.calculate_hash(data)) for data in complete_set]
        tree_depth = self.compute_tree_depth(len(old_set_of_nodes))

        for i in range(0, tree_depth):
            num_nodes = 2 ** (tree_depth - i)
            new_set_of_nodes = []
            for j in range(0, num_nodes, 2):
                child_node_0 = old_set_of_nodes[j]
                child_node_1 = old_set_of_nodes[j + 1]
                new_node = Node(
                    value=self.calculate_hash(
                        f"{child_node_0.value}{child_node_1.value}"
                    ),
                    left_child=child_node_0,
                    right_child=child_node_1,
                )
                new_set_of_nodes.append(new_node)
            old_set_of_nodes = new_set_of_nodes
        return new_set_of_nodes[0]