"""
LedgerEntry:
  Every ledger entry record creates 2 transactions
"""

from .transaction import Transaction

class LedgerEntry:
  def __init__(self, fromUser, toUser, amount):
    self.__creditTransaction = Transaction(fromUser, toUser, amount)
    self.__debitTransaction = Transaction(fromUser, toUser, amount * -1)

  @property
  def creditTransaction(self):
    return self.__creditTransaction

  @property
  def debitTransaction(self):
    return self.__debitTransaction

  @property
  def transactions(self):
    return [
      self.creditTransaction,
      self.debitTransaction,
    ]
