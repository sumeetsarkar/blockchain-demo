"""
BlockChain
"""

import json
from .block import Block
from .ledgerentry import LedgerEntry

class BlockChain:

  def __init__(self, name, difficulty, reward, filePath):
    self.__name = name
    self.__previousHashForGenesis = -1
    self.__chain = []
    self.__difficulty = difficulty
    self.__minerReward = reward
    if filePath:
      fileData = ''
      with open(filePath, 'rt') as f:
        for l in f.readlines():
          fileData += l
        jsonArray = json.loads(fileData)
        for jsonBlock in jsonArray:
          self.__chain.append(Block(jsonBlock))
    else:
      self.__chain.append(self.__create_genesis_block())


  # private method
  def __create_genesis_block(self):
    # create and return genesis block only if chain is empty
    if len(self.__chain) == 0:
      genesisblock = Block(None, [], self.__previousHashForGenesis, 0)
      genesisblock.mine()
      return genesisblock
    else:
      raise Exception('Genesis block can only be created when chain is empty')


  # private method
  def __get_last_block(self):
    # check if chain is empty
    if len(self.__chain) == 0:
      raise Exception('Empty chain')
    else:
      return self.__chain[len(self.__chain) - 1]


  def add_block(self, listOfTransactions, minerName):
    # check for block chain validity
    isValid, compromisedBlock = self.is_valid()
    if compromisedBlock is not None:
      raise Exception(self.__name + ' block chain is compromised!', isValid, compromisedBlock.summary)
    # get last block in chain
    lastBlockInChain = self.__get_last_block()
    # create new block with concatenated 1 reward transaction + list of transactions to add in block
    listOfTransactions = LedgerEntry(self.__name, minerName, self.__minerReward).transactions + listOfTransactions
    newBlock = Block(None, listOfTransactions, lastBlockInChain.hash, self.__difficulty)
    # Proof of Work Phase: mine new block with set diffculty
    newBlock.mine()
    # append newly mined block to the block chain
    self.__chain.append(newBlock)


  def is_valid(self):
    previousHash = self.__previousHashForGenesis
    for block in self.__chain:
      if block.is_hash_matching() is False:
        return False, block
      if block.is_merkel_matching() is False:
        return False, block
      if block.previousHash != previousHash:
        return False, block
      previousHash = block.hash
    return True, None


  def list_chain(self):
    for block in self.__chain:
      parsedTransaction = []
      for tran in block.listOfTransaction:
        parsedTransaction.append(tran.summary)
      parsedData = json.loads(json.dumps(block.summary))
      parsedData['transactions'] = parsedTransaction
      print(json.dumps(parsedData, indent=2))


  def compute_statement_for_user(self, user):
    totalDebit = 0
    totalCredit = 0
    print('\nLisiting ' + user + ' transactions...')
    for block in self.__chain:
      for tran in block.listOfTransaction:
        if tran.fromUser == user and tran.amount > 0:
          totalDebit -= tran.amount
          print(tran.summary)
        elif tran.toUser is user and tran.amount > 0:
          totalCredit += tran.amount
          print(tran.summary)
    print('Credits  : ' + str(totalCredit))
    print('Debits   : ' + str(totalDebit))
    print('Balance  : ' + str(totalCredit + totalDebit))
