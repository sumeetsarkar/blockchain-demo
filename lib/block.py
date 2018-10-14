"""
Block
"""

import hashlib

class Block:
  def __init__(self, listOfTransaction = [], previousHash = -1):
    self.__listOfTransaction = listOfTransaction
    self.__previousHash = previousHash
    self.__hash = -1
    self.__nounce = 0
  
  @property
  def listOfTransaction(self):
    return self.__listOfTransaction
  
  @property
  def previousHash(self):
    return self.__previousHash
  
  @property
  def hash(self):
    return self.__hash

  @property
  def summary(self):
    return dict(numTransactions=len(self.listOfTransaction),
                hash=self.hash,
                previousHash=self.previousHash,
    )

  # private method
  def __compute_hash(self):
    h = hashlib.sha256()
    h.update(str(self.__listOfTransaction) + str(self.__previousHash) + str(self.__nounce))
    return h.hexdigest()


  # private method
  def __generate_diffculty_string(self, difficulty):
    difficultyString = ''
    while difficulty is not 0:
      difficultyString += '0'
      difficulty -= 1
    return difficultyString


  def is_hash_matching(self):
    return self.hash == self.__compute_hash()


  def mine(self, difficulty):
    h = self.__compute_hash()
    difficultyString = self.__generate_diffculty_string(difficulty)
    # mine until the difficulty criteria is met with generated hash
    while h[0:int(difficulty)] is not difficultyString:
      # update nounce each time to generate different hash, which may meet the difficulty criteria
      self.__nounce += 1
      h = self.__compute_hash()
    # set the computed hash
    self.__hash = h

