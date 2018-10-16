"""
Block
"""

import json
import datetime
import hashlib

class Block:
  def __init__(self, listOfTransaction = [], previousHash = -1):
    self.__listOfTransaction = listOfTransaction
    self.__previousHash = previousHash
    self.__hash = -1
    self.__date = datetime.datetime.now()
    # below fields are to precompute static data for quicker __compute_hash iterations
    self.__listOfTransactionInJsonArray = self.__get_json_array_of_transactions()
    self.__strData = str(self.__previousHash) + str(self.__date.strftime('%c')) + self.__listOfTransactionInJsonArray
    # nounce is the only variable incrementer in hash
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

  #private method
  def __get_json_array_of_transactions(self):
    list = []
    for t in self.__listOfTransaction:
      list.append(t.summary)
    return json.dumps(list)

  # private method
  def __compute_hash(self):
    h = hashlib.sha256()
    strdata = self.__strData + str(self.__nounce)
    strdata = bytes(strdata, 'UTF8')
    h.update(strdata)
    return h.hexdigest()


  # private method
  def __generate_diffculty_string(self, difficulty):
    difficultyString = ''
    while difficulty is not 0:
      difficultyString += '0'
      difficulty -= 1
    return difficultyString


  def is_hash_matching(self):
    difficultyString = self.__generate_diffculty_string(self.__difficulty)
    return self.hash[0:int(self.__difficulty)] is difficultyString and self.hash == self.__compute_hash()


  def mine(self, difficulty):
    self.__difficulty = difficulty
    h = self.__compute_hash()
    difficultyString = self.__generate_diffculty_string(difficulty)
    # mine until the difficulty criteria is met with generated hash
    while h[0:int(difficulty)] is not difficultyString:
      # update nounce each time to generate different hash, which may meet the difficulty criteria
      self.__nounce += 1
      h = self.__compute_hash()
      # print(h, h[0:int(difficulty)], difficultyString)
    # set the computed hash
    self.__hash = h
