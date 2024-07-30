import os

from dotenv import load_dotenv
from web3 import *
from web3.contract import Contract
from web3.types import ABI, Address

# Initialize Web3 connection of Ethereum mainnet
load_dotenv()
w3 = Web3(Web3.HTTPProvider(os.environ['WEB3_PROVIDER']))

# Contract address
address = '4b4438eA9340f9dF6BBb13deb2129Ee8450b5F24'
contract_address: Address = Address(bytes.fromhex(address))

# Contract ABI
contract_abi: ABI = [{
    "type": "function",
    "name": "key",
    "inputs": [],
    "outputs": [{
        "name": "",
        "type": "string",
        "internalType": "string"
    }],
    "stateMutability": "view"
}]

# Get the contract instance
contract: Contract = w3.eth.contract(
    address=contract_address,
    abi=contract_abi
)

# Call the key() function of the contract
res = contract.functions.key().call()

# Convert the result to hex format
# b'upside academy forever 00\x00\x00A'
print(res.encode())

# hexify with 0x prefix
# 0x7570736964652061636164656d7920666f7265766572203030000041
print('0x' + res.encode().hex())
