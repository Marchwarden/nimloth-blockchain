from dataclasses import dataclass, field
import binascii
import base58
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA, RIPEMD160, SHA256 


# TODO: are these attributes meant to be immutable?


@dataclass
class Coin:
    name: str
    amount: int = 0

    def change_value(self, amount):
        if (self.amount + amount) < 0:
            return ValueError
        self.amount += amount
        return self.amount

# factory class for creating cointype subwallets for each chain
def coin_wallet_factory(on_chain=False, multiSignature=False, passPharase=False):
    print("creation of nimloth wallet")
    keys = ['public_key', 'chain_type','amount']
    if on_chain:
        print("creation of new onchain wallet")
        keys =['public_key','private_key','chain_type','amount','network', 'on_chain_public']
    if multiSignature:
        keys.append('cosigner1','cosigner2','cosigner3')
    if passPharase:
        keys.append('mnemonic')
    
    class CoinWallet(object):
        required_keys = set(keys)

        def __init__(self, **kwargs):
            self.coins = []
            if self.required_keys != set(kwargs.keys()):
                raise ValueError('Mismatch')
            # storing the keys and values to the credential object
            for k, v in kwargs.items():
                setattr(self, k, v)
        
    return CoinWallet
    
    

class UserWallet:
    # _private_key: RSA.RsaKey = RSA.generate(1024)
    # _public_key: RSA.RsaKey = _private_key.publickey()
    # _signer: pkcs1_15.PKCS115_SigScheme = pkcs1_15.new(_private_key)
    # multi layer encryption
    # dependant on account information different encryption systems are used, and then account recovery questions are used as keywords for further private generation
    def __init__(self, public_key):
        self.owner_public = public_key
        self.coins = []
        self.coinWallets = []
        ##switch from coins to outputs, the  add a wallet generation function, take a cointype so user objects bave a list of wallet objects of different coins
        self.address = self.wallet_address

    def new_coin(self, name, amount):
        _coin = Coin(name)
        if amount != 0:
            _coin.change_value(amount)
        return self.coins.append(_coin)
    
    def generate_new_coin_wallet(self, name, amount, onchain, multisig, mnemonic):
            if multisig:
              multisigniture = True  
            if mnemonic != "":
              passpharase = True 
            new_wallet = coin_wallet_factory(on_chain=onchain, multiSignature=multisigniture, passPharase=passpharase)
            coin_wallet = new_wallet(self.owner_public, name, amount)
    def search_for_coin(self, coin_name):
        for index, coin in enumerate(self.coins):
            if coin.name == coin_name:
                return index
        return -1

    @property
    def identity(self) -> str:
        return binascii.hexlify(
            self.owner_public.public_key.exportKey(format="DER")
        ).decode("ascii")
        
    @property
    def wallet_address(self):
        public_key = self.owner_public
        if type(public_key) == str:
            public_key = bytearray(public_key, "utf-8")
        hash_1 = SHA256.new()
        hash_1.update(public_key)
        hash_1=hash_1.hexdigest()
        if type(hash_1) == str:
            hash_1 = bytearray(hash_1, "utf-8")
        hash_2 = RIPEMD160.new()
        hash_2.update(hash_1)
        hash_2 =hash_2.hexdigest()
        return base58.b58encode(hash_2)

    # add authorization and authentification
    # I.E. proof of stake, proof of access to resourses, proof of authroization of transaction
