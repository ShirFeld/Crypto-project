import hashlib
from dataclasses import dataclass
import rsa
from typing import List

from Message import Message
import random

from utilities import get_fields_str



@dataclass
class Miner:
    amount: float
    private_key: rsa.PrivateKey
    public_key: rsa.PublicKey


    def update_sender_balance(self,tokens):
        if self.amount > tokens:
            self.amount = self.amount - tokens
            return True
        return False

    def update_reciver_balance(self,tokens):
        self.amount = self.amount + tokens

    def find_nonce_hash(self, nonce:str, block_number, transaction, previous_hash):
        counter = 1
        found = False

        while not found:
            result = get_fields_str(nonce, block_number, transaction, previous_hash, counter)
            # result = str(nonce) + str(block_number) + str(transaction ) + str(previous_hash) + str(counter)

            hash = hashlib.sha256(result.encode()).hexdigest()
            print(hash) # optional - for testing
            if hash[:4] == nonce:
                found = True
            counter += 1
        return hash

#--------------------------------------------------
users = List[Miner] # a list of all users and miners.

def get_miner_by_key(miners:List[Miner],public_key):
    """
    gives us the specific miner from miners list by miner id (public key).
    :param miners:
    :param public_key:
    :return:
    """
    for i in miners:
        if i.public_key.__eq__(public_key):
            return i

if __name__ == '__main__':
    (private_key, public_key) =  rsa.newkeys(128)
    (private_key2, public_key2) = rsa.newkeys(128)

    miner1 = Miner(200, private_key, public_key)
    miner2 = Miner(200, private_key2, public_key2)
    random = random.randint(1, 10000)

    # str(random.randint())
    message1 = Message(100, miner1.public_key, miner2.public_key, random)
    print(message1)

    miner1.find_nonce_hash('0000', 1000, message1.message_as_bytes(), message1.message_as_bytes())
