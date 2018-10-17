"""
Block
"""

import json
import time
import datetime
import hashlib

class Block:
  def __init__(self, listOfTransaction = [], previousHash = -1, difficulty = 0):
    self.__version = '1'
    self.__listOfTransaction = listOfTransaction
    self.__previousHash = previousHash
    self.__hash = -1
    self.__timeInSeconds = int(time.mktime(datetime.datetime.today().timetuple()))
    self.__difficulty = difficulty
    # below fields are to precompute static data for quicker __compute_hash iterations
    listOfTransactionInStringArray = self.__build_transactions_array_of_strings()
    # build merkel root of the transactions
    self.__merkelRoot = self.__build_merkel_root(listOfTransactionInStringArray)
    # build string concatenated data, used to compute block hash (except nounce)
    self.__strData = self.__version + str(self.__previousHash) + str(self.__merkelRoot) + str(self.__timeInSeconds)
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
    return dict(version=self.__version,
                previousHash=self.previousHash,
                merkelRoot=self.__merkelRoot,
                timeInSeconds=str(self.__timeInSeconds),
                hash=self.hash,
                nounce=self.__nounce,
                difficulty=self.__difficulty,
                numTransactions=len(self.listOfTransaction),
    )


  # private method
  def __build_sha256_hexdigest(self, strdata):
    b = bytes(strdata, 'UTF8')
    h = hashlib.sha256()
    h.update(b)
    return h.hexdigest()


  # private method
  def __build_transactions_array_of_strings(self):
    list = []
    for t in self.__listOfTransaction:
      list.append(json.dumps(t.summary))
    return list


  # private method
  def __build_merkel_root(self, list):
    n = len(list)
    if n == 1:
      return list[0]
    elif n == 0:
      return -1
    nextList = []
    if n % 2 != 0:
      l = n - 2
    else:
      l = n - 1
    for i in range(0, l, 2):
      leaf1 = self.__build_sha256_hexdigest(list[i])
      leaf2 = self.__build_sha256_hexdigest(list[i + 1])
      combinedLeaf = self.__build_sha256_hexdigest(leaf1 + leaf2)
      nextList.append(combinedLeaf)
    if l == n - 2:
      leafOdd = self.__build_sha256_hexdigest(list[n - 1])
      nextList.append(leafOdd)
    return self.__build_merkel_root(nextList)


  # private method
  def __compute_hash(self):
    strdata = self.__strData + str(self.__nounce)
    # SHA256(SHA256(Block_Header))
    return self.__build_sha256_hexdigest(str(self.__build_sha256_hexdigest(strdata)))


  # private method
  def __generate_diffculty_string(self):
    difficultyString = ''
    difficulty = self.__difficulty
    while difficulty != 0:
      difficultyString += '0'
      difficulty -= 1
    return difficultyString


  def is_hash_matching(self):
    difficultyString = self.__generate_diffculty_string()
    return self.hash[0:int(self.__difficulty)] == difficultyString and self.hash == self.__compute_hash()


  def mine(self):
    print('\n\nMining new block chain with difficulty: ' + str(self.__difficulty))
    h = self.__compute_hash()
    difficultyString = self.__generate_diffculty_string()
    # mine until the difficulty criteria is met with generated hash
    while h[0:int(self.__difficulty)] != difficultyString:
      # update nounce each time to generate different hash, which may meet the difficulty criteria
      self.__nounce += 1
      h = self.__compute_hash()
    # set the computed hash
    self.__hash = h
