> Sample BlockChain demo lib in python

## Quickstart

### [main.py](main.py) demostrates sample usage of BlockChain package

Run app
```
python3 main.py
```

Run test
```
python3 -m unittest tests/test_blockchain.py
```

## Package usage
### [BlockChain](libbc/blockchain.py)

The class BlockChain is used as a context manager

Upon instantiation it,
  - Reads & loads the yaml config
  - If run in testMode, all operations are in memory and previous blockchain state is neither read from file, nor new blocks are dumped to file on end
  - However, testMode or not, if the loaded chain is empty, a genesis block is created and transactions are accepted so on 

```python
from libbc import BlockChain

configPath = <your_config.yml_path>
currentDir = <dir_path_to_save_blockchain>

with BlockChain(configPath, currentDir) as bc:

  # add transactions to the block chain,
  # arg1: transaction array
  # arg2: miner account
  # Note: every add block call to blockchain
  # adds a ledger entry of the miner reward
  bc.add_block([], 'sumeetsarkar')
  
  # list the block chain so far in json
  bc.list_chain()

  # checks for validity of the block chain
  # returns tuple
  # True, None
  # False, Corrupted Block instance 
  # Blockchain is first validated before every block addition
  bc.is_valid()

  # prints account summary of transactions for given user
  # returns tuple, (totalCredit, totalDebit)
  bc.compute_statement_for_user('userA')
```

### [LedgerEntry](libbc/ledgerentry.py)

Each [LedgerEntry](libbc/ledgerentry.py) is recorded as two transactions using class [Transaction](libbc/transaction.py)

```python
from libbc import LedgerEntry

le = LedgerEntry('userA', 'userB', 400)

# transactions is a property of LE, returning the array of transactions in ledger
le.transactions
```

## [BlockChain Config](config.yml)
```yaml
# Block chain config

name: <your-blockchain-name>

# block mining difficulty
difficulty: 4

# miner reward
reward: 10

# test mode false, does not dump or read blockchain file
# transactions are volatile
testMode: false


# file dump configs
dump:
  dir: data
  # if filename is null, use blockchain name
  file: null
  # frequency of dump, after every 'block', or 'end'
  frequency: block

```

## Block Definition from BlockChain

Following information is captured in every block
- Block version
- Previous block hash
- Block hash
- Merkel root of transactions (includes miner reward)
- Time in seconds of request for block creation
- Nounce
- Difficulty
- Number of transactions
- List of transactions


## Hash Algorithm

### SHA256(SHA256(Block_Header))

Block_Header = (version + previousHash + merkelRoot + timeInSeconds + Nounce)


## Sample Block

```json
{
    "version": "1",
    "previousHash": "837dd71bf9814c03689aad9a9c963df41421de96fe40dae2e1b56898d3aeb5c7",
    "merkelRoot": "e6b8da89aa107105dd309131ebf607f875c135bacc4d030205794e224b1f7d01",
    "timeInSeconds": "1539871539",
    "hash": "000094fb9324ccf419b6c8eee13c068dcf24d7976d47839c1c7d73daf35c4f9a",
    "nounce": 35955,
    "difficulty": 4,
    "numTransactions": 6,
    "transactions": [
      {
        "fromUser": "sumeet-blockchain",
        "toUser": "sumeetsarkar",
        "amount": 10
      },
      {
        "fromUser": "sumeetsarkar",
        "toUser": "sumeet-blockchain",
        "amount": -10
      },
      {
        "fromUser": "userA",
        "toUser": "userB",
        "amount": 400
      },
      {
        "fromUser": "userB",
        "toUser": "userA",
        "amount": -400
      },
      {
        "fromUser": "userA",
        "toUser": "userC",
        "amount": 200
      },
      {
        "fromUser": "userC",
        "toUser": "userA",
        "amount": -200
      }
    ]
  },
```