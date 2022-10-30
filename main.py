import hashlib

class NimlothCoinBlock:
    def __init__(self, previous_block_hash, transaction_list):
        self.previous_block_hash = previous_block_hash
        self.transactions_list = transaction_list

        self.block_data ="-".join(transaction_list) + "-" + previous_block_hash
        self.block_hash = hashlib.sha256(self.block_data.encode()).hexdigest()


t1 = "User1 sends 5 NC to User2"
t2 = "User2 sends 24 NC to User3"
t3 = "User3 sends 12 NC to User4"
t4 = "User2 sends 31 NC to User1"

genesis_block = NimlothCoinBlock("Initial String", [t1, t2])
print(genesis_block.block_data)
print(genesis_block.block_hash)

second_block = NimlothCoinBlock(genesis_block.block_hash, [t3,t4])
print(second_block.block_data)
print(second_block.block_hash)