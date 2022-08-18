import hashlib
from dataclasses import dataclass
import rsa
from typing import List


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

    def find_hash_nonce(self, nonce:str, block_number, transaction, previous_hash):
        counter = 1
        found = False

        while not found:
            result = str(nonce) + str(block_number) + transaction + previous_hash + counter
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

    (private_key,public_key) =  rsa.newkeys(128)
    print(private_key)
    print(public_key)
    miner1 = Miner(200,private_key, public_key)

    # print(miner1)
    # Miner.find_hash_nonce()