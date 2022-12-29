import json

from ..block_files.blockchain import Blockchain
from ..block_files.block import NimlothBlock

FILENAME = "blockchainjson"


def get_blockchain_from_memory():
    with open(FILENAME, "r") as file_obj:
        blocks_text = file_obj.read()
        block_list = json.loads(blocks_text)
        block_chain = Blockchain([], [], 2)
        previous_block = None
        for block_dict in reversed(block_list):
            blockdata = block_dict.get("blockdata")
            newblock = NimlothBlock(
                blockdata.get("index"),
                blockdata.get("hash"),
                blockdata.get("previous_hash"),
                blockdata.get("timestamp"),
                blockdata.get("nonce"),
                blockdata.get("transactions"),
            )
            block_chain.chain.append(newblock)
    return block_chain


def get_block_from_memory(block_object):
    json.loads(block_object)


def store_blockchain_in_memory(blockchain: Blockchain):
    text = json.dumps(blockchain.to_dict()).encode("utf-8")
    with open("blockchaintes", "wb") as file_obj:
        file_obj.write(text)
