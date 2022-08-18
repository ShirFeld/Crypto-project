from dataclasses import dataclass
import dataclasses as dc
from datetime import datetime
from typing import List
import exceptions
import rsa
from utilities import get_fields_str
import hashlib
from Message import Message
from random import random


@dataclass
class Block:
    prev_block_hash: str
    index: int
    messages: List[Message]
    current_block_hash: str = dc.field(init=False)
    time_added: datetime = dc.field(init=False)
    nonce: str = dc.field(init=False)  # this var is the riddle \ תעלומה

    TOKEN_PRIZE = 3  # for the miner

    def compute_block_header(self) -> bytes:
        block_str = \
            get_fields_str(self.prev_block_hash, self.index, self.messages, self.time_added, self.nonce)
        return block_str.encode()

    def compute_block_hash(self) -> str:
        """
        computes the hash of the block using SHA-256 algorithm
        :return: the hash in hexadecimal
        """
        self.make_nonce()  # create a nonce to the block
        block_hash = hashlib.sha256(self.compute_block_header()).hexdigest()
        self.current_block_hash = block_hash
        return block_hash

    def make_nonce(self):
        """Generate pseudorandom number."""
        self.nonce = str(random.randint(1000, 10000))
        return self.nonce

    # def validate_block(self, miner_proof: Callable[[bytes], bool]) -> bool:
