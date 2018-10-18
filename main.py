"""
Demonstrates usage of the BlockChain demo library
"""

import os
from libbc import BlockChain
from libbc import LedgerEntry

# create block chain instance with difficulty 1 and reward 10 units
currentDir = os.path.dirname(__file__)
configPath = os.path.join(currentDir, 'config.yml')

with BlockChain(configPath, currentDir) as bc:
  # create list of transactions from ledger entry
  listOfTransactions = []
  listOfTransactions += LedgerEntry('userA', 'userB', 400).transactions
  listOfTransactions += LedgerEntry('userA', 'userC', 200).transactions
  # add list of transactions to the block chain
  bc.add_block(listOfTransactions, 'sumeetsarkar')

  # list the entire block chain so far
  print('\n\nBlock chain so far...')
  print('---------------------')
  bc.list_chain()

  # create list of transactions from ledger entry
  listOfTransactions = []
  listOfTransactions += LedgerEntry('userA', 'userB', 900).transactions
  listOfTransactions += LedgerEntry('userC', 'userD', 500).transactions
  # add list of transactions to the block chain
  bc.add_block(listOfTransactions, 'sumeetsarkar')

  # list the entire block chain so far
  print('\n\nBlock chain so far...')
  print('---------------------')
  bc.list_chain()

  # check the validity of the block chain
  print('\n\nBlock chain validity', bc.is_valid())

  bc.compute_statement_for_user('userA')
  bc.compute_statement_for_user('userB')
  bc.compute_statement_for_user('userC')
  bc.compute_statement_for_user('userD')
  bc.compute_statement_for_user('sumeetsarkar')
  bc.compute_statement_for_user('sumeet-blockchain')
