"""
BlockChain
"""

import os
import json
import yaml
from .block import Block
from .ledgerentry import LedgerEntry

class BlockChain:

  def __init__(self, configPath):
    if configPath is None:
      raise Exception('Config file Path missing')
    self.__configPath = configPath


  def __enter__(self):
    try:
      # read yaml file and load
      with open(self.__configPath) as f:
        self.__ymlConfig = next(yaml.load_all(f))
        self.__applyConfig()
        return self
    except Exception as e:
      print('Error reading config file', self.__configPath, e)


  def __exit__(self, *args):
    self.dump_blockchain_to_file()


  def __applyConfig(self):
    # initialize empty chain
    self.__chain = []
    # load values from yaml file
    self.__name = self.__ymlConfig['name']
    self.__difficulty = self.__ymlConfig['difficulty']
    self.__minerReward = self.__ymlConfig['reward']
    self.__previousHashForGenesis = self.__ymlConfig.get('genesisPreviousHash', -1)
    self.__testMode = self.__ymlConfig['testMode']
    # check if file dump config is specified, mandatory if testMode is False
    if self.__ymlConfig.get('dump') is None and self.__testMode is False:
      raise Exception('No file dump information specified in config')
    if self.__testMode is False:
      dirname = self.__ymlConfig.get('dump')['dir']
      filename = self.__ymlConfig.get('dump').get('file')
      if filename is None:
        filename = self.__name
      filename += '.json'
      # form file dump path
      self.__filePath = os.path.join(os.path.dirname(__file__), '../', dirname, filename)
      self.__load_blockchain_from_file()
    else:
      self.__chain.append(self.__create_genesis_block())


  def __load_blockchain_from_file(self):
    """Loads previously saved blockchain json from file
    If file is empty/ or read error, creates genesis block and starts the chain
    """
    try:
      with open(self.__filePath, 'rt') as f:
        jsonArray = json.load(f)
        for jsonBlock in jsonArray:
          self.__chain.append(Block(jsonBlock))
    except Exception as e:
      print('Error loading blockchain from file', self.__filePath, e)
    finally:
      if len(self.__chain) == 0:
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
    if isValid is False:
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
    # self.dump_blockchain_to_file()


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


  def dump_blockchain_to_file(self):
    if self.__filePath is None:
      return
    jsonArray = []
    for block in self.__chain:
      parsedTransaction = []
      for tran in block.listOfTransaction:
        parsedTransaction.append(tran.summary)
      parsedData = json.loads(json.dumps(block.summary))
      parsedData['transactions'] = parsedTransaction
      jsonArray.append(parsedData)
    with open(self.__filePath, 'w+') as f:
      json.dump(jsonArray, f, indent=2)


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
        elif tran.toUser == user and tran.amount > 0:
          totalCredit += tran.amount
          print(tran.summary)
    print('Credits  : ' + str(totalCredit))
    print('Debits   : ' + str(totalDebit))
    print('Balance  : ' + str(totalCredit + totalDebit))
