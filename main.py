from lib import BlockChain
from lib import Transaction

blockChain = BlockChain('sumeet-blockchain', 1, 10)

listOfTransactions = [
  Transaction('userA', 'userB', 400),
  Transaction('userC', 'userD', 100),
  Transaction('userA', 'userC', 200),
]
blockChain.add_block(listOfTransactions, 'sumeetsarkar')

listOfTransactions = [
  Transaction('userA', 'userB', 900),
  Transaction('userC', 'userD', 500),
]
blockChain.add_block(listOfTransactions, 'sumeetsarkar')

blockChain.list_chain()

print('Block chain validity', blockChain.is_valid() is None)
