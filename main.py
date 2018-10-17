from lib import BlockChain
from lib import LedgerEntry

# create block chain instance with difficulty 1 and reward 10 units
blockChain = BlockChain('sumeet-blockchain', 6, 10)

# create list of transactions from ledger entry
listOfTransactions = []
listOfTransactions += LedgerEntry('userA', 'userB', 400).transactions
listOfTransactions += LedgerEntry('userA', 'userC', 200).transactions
# add list of transactions to the block chain
blockChain.add_block(listOfTransactions, 'sumeetsarkar')

# list the entire block chain so far
print('\n\nBlock chain so far...')
print('---------------------')
blockChain.list_chain()

# create list of transactions from ledger entry
listOfTransactions = []
listOfTransactions += LedgerEntry('userA', 'userB', 900).transactions
listOfTransactions += LedgerEntry('userC', 'userD', 500).transactions
# add list of transactions to the block chain
blockChain.add_block(listOfTransactions, 'sumeetsarkar')

# list the entire block chain so far
print('\n\nBlock chain so far...')
print('---------------------')
blockChain.list_chain()

# check the validity of the block chain
print('Block chain validity', blockChain.is_valid() is None)

blockChain.compute_statement_for_user('userA')
blockChain.compute_statement_for_user('userC')
blockChain.compute_statement_for_user('sumeetsarkar')
