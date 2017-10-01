#!/usr/bin/env python3

from flask import Flask
from flask import request
from block import Block
from block import Blockchain
import copy
import datetime as time
import json

node = Flask(__name__)

this_node_transactions = []
peer_nodes = [
    "localhost:5000",
]
mining = True
this_chain = Blockchain()

@node.route("/txion", methods=['POST'])
def transaction():
    if request.method == 'POST':
        new_txion = request.get_json()
        this_node_transactions.append(new_txion)
        print("New transaction")
        print("FROM: {}".format(new_txion['from']))
        print("TO: {}".format(new_txion['to']))
        print("AMOUNT: {}".format(new_txion['amount']))
        return "Transction submission successful\n"

miner_address = "q3nf394hjg-random-miner-address-34nf3i4nflkn3oi"

@node.route('/mine', methods = ['GET'])
def mine():
    last_block = this_chain.blockchain[-1]
    # print(type(last_block))
    last_proof = (last_block).data['proof_of_work']
    proof = proof_of_work(last_proof)
    this_node_transactions.append(
        { "from": "network", "to": miner_address, "amount": 1 }
    )

    new_block_data = {
        "proof_of_work": proof,
        "transactions": list(this_node_transactions)
    }

    this_node_transactions[:] = []
    
    mined_block = this_chain.add_block(new_block_data)

    return json.dumps({
        "index": mined_block.index,
        "timestamp": str(mined_block.timestamp),
        "data": mined_block.data,
        "hash": mined_block.hash,
    }) + "\n"

@node.route("/blocks", methods=["GET"])
def get_blocks():
    chain_to_send = copy.deepcopy(this_chain.blockchain)

    for i in range(len(chain_to_send)):
        block = chain_to_send[i]
        chain_to_send[i] = {
            "index": str(block.index),
            "timestamp": str(block.timestamp),
            "data": str(block.data),
            "hash": block.hash
        }

    my_chain = json.dumps(chain_to_send)
    return my_chain

def find_new_chain():
    other_chains = []
    for node_url in peer_nodes:
        chain = request.get(node_url + '/blocks').content
        chain = json.loads(chain)
        other_chains.append(chain)
    return other_chains


def consensus():
    other_chains = find_new_chain()
    longest_chain = this_chain.blockchain

    for chain in other_chains:
        if len(longest_chain) < len(chain):
            longest_chain = chain

    this_chain.blockchain = longest_chain

def proof_of_work(last_proof):
    incrementor = last_proof + 1
    while not (incrementor % 9 == 0 and incrementor % last_proof == 0):
        incrementor += 1

    return incrementor

node.run()