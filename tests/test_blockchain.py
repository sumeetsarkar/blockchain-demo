"""
Validates the sample block chain
"""

import os
import json
import unittest

from libbc import BlockChain

class TestBlockChainMethods(unittest.TestCase):

  def setUp(self):
    # prepare file paths
    self.__currentDir = os.path.dirname(__file__)
    self.__configValid = os.path.join(self.__currentDir, 'config/valid', 'config.yml')
    self.__configInvalidCorruptHash = os.path.join(self.__currentDir, 'config/invalid', 'config_corrupt_hash.yml')
    self.__configInvalidCorruptPreviousHash = os.path.join(self.__currentDir, 'config/invalid', 'config_corrupt_previous_hash.yml')
    self.__configInvalidCorruptTransaction = os.path.join(self.__currentDir, 'config/invalid', 'config_corrupt_transactions.yml')
  
  def test_valid(self):
    with BlockChain(self.__configValid, self.__currentDir) as bc:
      result = bc.is_valid()
      self.assertTrue(result[0])
      self.assertIsNone(result[1])
    
  def test_invalid_hash(self):
    with BlockChain(self.__configInvalidCorruptHash, self.__currentDir) as bc:
      result = bc.is_valid()
      self.assertFalse(result[0])
      self.assertIsNotNone(result[1])

  def test_invalid_previous_hash(self):
    with BlockChain(self.__configInvalidCorruptPreviousHash, self.__currentDir) as bc:
      result = bc.is_valid()
      self.assertFalse(result[0])
      self.assertIsNotNone(result[1])

  def test_invalid_corrupt_transaction(self):
    with BlockChain(self.__configInvalidCorruptTransaction, self.__currentDir) as bc:
      result = bc.is_valid()
      self.assertFalse(result[0])
      self.assertIsNotNone(result[1])
    
  def test_compute_statement_for_user(self):
    with BlockChain(self.__configValid, self.__currentDir) as bc:
      totalCredit, totalDebit = bc.compute_statement_for_user('userA', False)
      self.assertEqual(totalCredit, 0)
      self.assertEqual(totalDebit, -3000)
      totalCredit, totalDebit = bc.compute_statement_for_user('userC', False)
      self.assertEqual(totalCredit, 400)
      self.assertEqual(totalDebit, -1000)

if __name__ == '__main__':
    unittest.main()
