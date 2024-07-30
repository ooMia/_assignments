import os

from dotenv import load_dotenv
from web3 import *
from web3.types import Address

# Initialize Web3 connection of Ethereum mainnet
load_dotenv()
w3 = Web3(Web3.HTTPProvider(os.environ['WEB3_PROVIDER']))

# Contract address
address = '4b4438eA9340f9dF6BBb13deb2129Ee8450b5F24'
contract_address: Address = Address(bytes.fromhex(address))

# https://web3py.readthedocs.io/en/stable/web3.eth.html#web3.eth.Eth.get_storage_at
storage_pos = int('0x1337deadbeef', 16)  # 0x1337deadbeef
print(storage_pos)
res = w3.eth.get_storage_at(contract_address, storage_pos)

# Convert the result to hex format
print(res)
print(res.hex())
print(len(res))
