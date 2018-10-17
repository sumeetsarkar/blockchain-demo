"""
Validates the sample block chain
"""

import os
import json
import unittest

from lib import BlockChain

class TestBlockChainMethods(unittest.TestCase):

  def setUp(self):
    # prepare file paths
    self.__filePathValid = os.path.join(os.path.dirname(__file__), 'data/valid', 'valid_blockchain.json')
    self.__filePathInvalidCorruptHash = os.path.join(os.path.dirname(__file__), 'data/invalid', 'invalid_blockchain_corrupt_hash.json')
    self.__filePathInvalidCorruptPreviousHash = os.path.join(os.path.dirname(__file__), 'data/invalid', 'invalid_blockchain_corrupt_previous_hash.json')
    self.__filePathInvalidCorruptTransaction = os.path.join(os.path.dirname(__file__), 'data/invalid', 'invalid_blockchain_corrupt_transactions.json')
  
  def test_valid(self):
    blockChainValid = BlockChain('test_valid', 6, 10, self.__filePathValid)
    result = blockChainValid.is_valid()
    self.assertTrue(result[0])
    self.assertIsNone(result[1])
    
  def test_invalid_hash(self):
    blockChainInvalidCorruptHash = BlockChain('test_invalid', 6, 10, self.__filePathInvalidCorruptHash)
    result = blockChainInvalidCorruptHash.is_valid()
    self.assertFalse(result[0])
    self.assertIsNotNone(result[1])

  def test_invalid_previous_hash(self):
    blockChainInvalidCorruptPreviousHash = BlockChain('test_invalid', 6, 10, self.__filePathInvalidCorruptPreviousHash)
    result = blockChainInvalidCorruptPreviousHash.is_valid()
    self.assertFalse(result[0])
    self.assertIsNotNone(result[1])

  def test_invalid_corrupt_transaction(self):
    blockChainInvalidCorruptTransaction = BlockChain('test_invalid', 6, 10, self.__filePathInvalidCorruptTransaction)
    result = blockChainInvalidCorruptTransaction.is_valid()
    self.assertFalse(result[0])
    self.assertIsNotNone(result[1])
    

if __name__ == '__main__':
    unittest.main()
