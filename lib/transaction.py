"""
Transaction
"""

class Transaction:
  def __init__(self, fromUser, toUser, amount):
    self.__fromUser = fromUser
    self.__toUser = toUser
    self.__amount = amount

  @property
  def fromUser(self):
    return self.__fromUser

  @property
  def toUser(self):
    return self.__toUser

  @property
  def amount(self):
    return self.__amount

  @property
  def summary(self):
    return dict(fromUser=self.fromUser,
                toUser=self.toUser,
                amount=self.amount,
    )
