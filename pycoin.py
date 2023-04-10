import hashlib
import time

from utils import generate_key_pair, sign_message, verify_signature


class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        """
        Initialize a block with the given attributes.
        :param index: The position of the block in the blockchain.
        :param previous_hash: The hash of the previous block in the chain.
        :param timestamp: The time the block was created.
        :param data: The data stored in the block.
        :param hash: The hash of the block.
        """
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash
        self.nonce = None


class Blockchain:
    def __init__(self):
        """
        Initialize the blockchain with a genesis block.
        """
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []  
        self.difficulty = 1
        self.miner_reward = 50

    def create_genesis_block(self):
        """
        Create the first (genesis) block of the blockchain.
        :return: The genesis block.
        """
        return Block(0, "0", time.time(), "Genesis Block", None)



    def add_block(self, transactions):
        """
        Add a new block with the given transactions to the blockchain.
        :param transactions: A list of transactions to be stored in the new block.
        """
        previous_block = self.chain[-1]
        # print('here1')
        new_block = Block(len(self.chain), previous_block.hash, time.time(), transactions, None)
        new_block.nonce = self.proof_of_work(new_block)
        new_block.hash = self.calculate_hash(new_block)

        # Check if the calculated hash is valid and if the block is valid before appending to the chain.
        if self.is_hash_valid(new_block.hash) and self.is_block_valid(new_block, previous_block):
            self.chain.append(new_block)


    
    def calculate_hash(self, block):
        """
        Calculate the hash for a block based on its attributes.
        :param block: The block for which the hash is to be calculated.
        :return: The hash of the block.
        """
        block_data = str(block.index) + str(block.previous_hash) + str(block.timestamp) + str(block.data) + str(block.nonce)
        return hashlib.sha256(block_data.encode('utf-8')).hexdigest()


    def is_chain_valid(self):
        """
        Check if the blockchain is valid by verifying the hashes and previous hashes of each block.
        :return: True if the blockchain is valid, False otherwise.
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != self.calculate_hash(current_block):
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True
    
    
    def is_block_valid(self, block, previous_block):
        """
        Check if the given block is valid by verifying its hash, previous hash, and proof of work.
        :param block: The block to be validated.
        :param previous_block: The previous block in the chain.
        :return: True if the block is valid, False otherwise.
        """
        if previous_block.hash != block.previous_hash:
            return False
    
        if self.calculate_hash(block) != block.hash:
            return False
    
        if not self.is_hash_valid(block.hash):
            return False
    
        return True

        
    def is_hash_valid(self, block_hash):
        """
        Check if a block's hash is valid by verifying that it starts with the correct number of leading zeros.
        :param block_hash: The hash of a block.
        :return: True if the block's hash is valid, False otherwise.
        """
        return block_hash.startswith("0" * self.difficulty)


    def proof_of_work(self, block, difficulty=1):
        """
        Calculate the proof-of-work for the given block with the specified difficulty.
        :param block: The block for which to calculate the proof-of-work.
        :param difficulty: The number of leading zeros required in the block hash.
        :return: The nonce that satisfies the proof-of-work condition.
        """
        nonce = 0
        while True:
            # print('here!')
            block.nonce = nonce
            block_hash = self.calculate_hash(block)
            print(block_hash)
            if block_hash.startswith("0" * difficulty):
                return nonce
            nonce += 1

    def validate_transaction(self, transaction):
        if transaction.sender is None:
            return True  # Assume this is a coinbase transaction (reward for mining a new block)

        message = f"{transaction.sender}-{transaction.receiver}-{transaction.amount}"
        return verify_signature(transaction.sender, message, transaction.signature)

    def resolve_conflicts(self, other_chains):
        """
        Resolve conflicts between the current chain and other chains by choosing the longest valid chain.
        :param other_chains: A list of other blockchain instances to compare with the current chain.
        """
        longest_chain = self.chain
        max_length = len(self.chain)

        for chain in other_chains:
            if len(chain) > max_length and self.is_chain_valid():
                max_length = len(chain)
                longest_chain = chain

        self.chain = longest_chain





class Transaction:

    def __init__(self, sender, receiver, amount):
        """
        Initialize a transaction with the given attributes.
        :param sender: The sender's address.
        :param receiver: The receiver's address.
        :param amount: The amount of PyCoin being transferred.
        """
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.signature = None

    def sign(self, private_key):
        message = f"{self.sender}-{self.receiver}-{self.amount}"
        self.signature = sign_message(private_key, message)