from dataclasses import dataclass
import dataclasses as dc
from datetime import datetime
from typing import List
from exceptions import TransactionException
from exceptions import BlockException
from utilities import get_fields_str
import hashlib
from Message import Message

@dataclass
class Block:
    prev_block_hash: str
    index: int
    messages: List[Message]
    current_block_hash: str = dc.field(init=False)
    time_added: datetime = dc.field(init=False)

    TOKEN_PRIZE = 3  # for the miner

    def compute_block_header(self) -> bytes:
        block_str = \
            get_fields_str(self.prev_block_hash, self.index, self.messages, self.time_added)
        return block_str.encode()

    def compute_block_hash(self) -> str:
        """
        computes the hash of the block using SHA-256 algorithm
        :return: the hash in hexadecimal
        """
        block_hash = hashlib.sha256(self.compute_block_header()).hexdigest()
        self.current_block_hash = block_hash
        return block_hash


    # def validate_block(self, miner_proof: Callable[[bytes], bool]) -> bool:

    def validate_block(self)->bool:
        for index, transaction in enumerate(self.messages):
            try:
                transaction.verify_message()
                if index > 0 and transaction.message_signature != self.messages[index - 1].message_signature:
                    raise BlockException("Block creation failed due linking problem in transaction number: "
                                         + index)
            except TransactionException as tte:
                raise BlockException("Block creation failed due to validation problem in transaction number: "
                                     + index + str(tte))
        return True