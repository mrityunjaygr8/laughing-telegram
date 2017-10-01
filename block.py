#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import hashlib as hasher
import datetime as date

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def hash_block(self):
        sha = hasher.sha256()
        sha.update(self.block_utf8())
        return sha.hexdigest()

    def block_utf8(self):
        return (str(self.index) + \
                str(self.timestamp) + \
                str(self.data) + \
                str(self.previous_hash)).encode('utf-8')

    def __str__(self):
        return "Block {0}:\n{1}".format(self.hash, self.data)


class Blockchain(object):
    blockchain = [Block(0, date.datetime.now(), {"proof_of_work": 1, "genesis": True}, "0")]

    def add_block(self, data):
        new_block = Block(
            self.blockchain[-1].index + 1,
            date.datetime.now(),
            data,
            self.blockchain[-1].hash    
        )
        self.blockchain.append(new_block)
        return new_block

def main():
    snake_coin = Blockchain()

    for i in range(20):
        block = snake_coin.add_block("Hey! I\'m block #{}".format(i))
        print("Block #{} has been added to the blockchain!".format(block.index))
        print("Data: {}".format(block.data))
        print("Hash: {}\n".format(block.hash))

    print(snake_coin.blockchain[-1])


if __name__ == '__main__':
    main()