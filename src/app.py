from flask import Flask
from dataclasses import dataclass, field
import json
from UserClass import User
from TransactionClass import Transaction
from NimlothBlockClass import NimlothBlock
from BlockchainClass import Blockchain

app = Flask(__name__)

NimlothBlockchain = Blockchain()
transactions = []
last_block_hash = ""

@app.route('/') 
def test_message(): 
   return '<h1>Sup2</h1>'

if __name__ == "__main__": 
   app.run(debug=True, host='0.0.0.0', port=8000)

def display_transaction(transaction):
    for transaction in transactions:
        dict = transaction.to_dict()
        print ("sender: " + dict['sender'])
        print ('-----')
        print ("recipient: " + dict['recipient'])
        print ('-----')
        print ("value: " + str(dict['value']))
        print ('-----')
        print ("time: " + str(dict['time']))
        print ('-----')
        print ('--------------')

# TODO: this isn't correct 
@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)

    return json.dumps({"length": len(chain_data), "chain": chain_data})


charles = User()
print(charles.identity)
jack = User()
print(jack.identity)

t0 = Transaction(
    "Genesis",
    charles.identity,
    500.0
)

# block0 = NimlothBlock()
# block0.previous_block_hash = None
# Nonce = None

print("public key") 
print(charles._public_key)
print("Private Key")
print(charles._private_key)
print(" Identity") 
print(charles.identity)

#block0.verified_transactions_list.append(t0)
#digest = hash(block0)
#last_block_hash = digest

#NimlothBlockchain.append(block0)

#signature = t0.sign_transaction()
#print(signature)
#transactions.append(t)
#display_transaction(t)