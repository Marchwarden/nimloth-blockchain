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
    def __init__(self, value: str, left_child=None, right_child=None):
        self.value = value
        self.left_child = left_child
        self.right_child = right_child


class Transactiontree:
    def __init__(self, transactions):
        self.merkle_hash: str
        self.nodes = []
        self.transactions = []

    def calculate_hash(self, data) -> str:
        transaction_string = json.dumps(data.__dict__, sort_keys=True)
        return SHA.new(transaction_string.encode()).hexdigest()

    def hash_transactions(self, transactions):
        for i in transactions:
            self.transactions.append(self.calculate_hash(i))

    def compute_tree_depth(self, number_of_leaves: int) -> int:
        return math.ceil(math.log2(number_of_leaves))

    def is_power_of_2(self, number_of_leaves: int) -> bool:
        return math.log2(number_of_leaves).is_integer()

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

    def build_merkle_tree(self) -> Node:
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