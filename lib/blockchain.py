"""
BlockChain
"""

import json
from block import Block
from transaction import Transaction

class BlockChain:

  def __init__(self, name, difficulty, reward):
    self.__name = name
    self.__previousHashForGenesis = -1
    self.__chain = []
    self.__pendingTransaction = []
    self.__difficulty = difficulty
    self.__minerReward = reward
    self.__chain.append(self.__create_genesis_block())


  # private method
  def __create_genesis_block(self):
    # create and return genesis block only if chain is empty
    if len(self.__chain) is 0:
      genesisblock = Block([], self.__previousHashForGenesis)
      genesisblock.mine(self.__difficulty)
      return genesisblock
    else:
      raise Exception('Genesis block can only be created when chain is empty')


  # private method
  def __get_last_block(self):
    # check if chain is empty
    if len(self.__chain) is 0:
      raise Exception('Empty chain')
    else:
      return self.__chain[len(self.__chain) - 1]


  def add_block(self, listOfTransactions, minerName):
    # check for block chain validity
    compromisedBlock = self.is_valid()
    if compromisedBlock is not None:
      raise Exception(self.__name + ' block chain is compromised!', compromisedBlock)
    # get last block in chain
    lastBlockInChain = self.__get_last_block()
    # create new block with concatenated list of pending transaction + current transactions
    newBlock = Block(self.__pendingTransaction + listOfTransactions, lastBlockInChain.hash)
    # Proof of Work Phase: mine new block with set diffculty
    newBlock.mine(self.__difficulty)
    # append newly mined block to the block chain
    self.__chain.append(newBlock)
    # add miner reward transaction in the pending transaction
    self.__pendingTransaction = [
      Transaction(self.__name, minerName, self.__minerReward)
    ]


  def is_valid(self):
    previousHash = self.__previousHashForGenesis
    for block in self.__chain:
      if block.is_hash_matching() is False:
        return block
      if block.previousHash is not previousHash:
        return block
      previousHash = block.hash
    return None


  def list_chain(self):
    for block in self.__chain:
      parsedTransaction = []
      for tran in block.listOfTransaction:
        parsedTransaction.append(tran.summary)
      parsedData = json.loads(json.dumps(block.summary))
      parsedData['transactions'] = parsedTransaction
      print(json.dumps(parsedData, indent=2))


  def compute_statement_for_user(self, user):
    # TODO
    pass
