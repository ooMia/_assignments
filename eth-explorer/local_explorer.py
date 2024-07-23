from hexbytes import HexBytes
from web3 import Web3
from web3.datastructures import AttributeDict
from web3.exceptions import BlockNotFound

from web3.types import TxReceipt, BlockData

rpc_url = 'http://host3.dreamhack.games:21773/8eb75107dd3c/rpc'
w3 = Web3(Web3.HTTPProvider(rpc_url))
assert w3.is_connected()

for block_number in range(100):
    try:
        block: BlockData = w3.eth.get_block(block_number, full_transactions=True)
    except BlockNotFound:
        continue
    for tx in block.get('transactions'):
        tx: AttributeDict = tx
        tx_hash: HexBytes = tx.get('hash')

        print(tx_hash.hex())
        # receipt: TxReceipt = w3.eth.get_transaction_receipt(tx_hash)
        # print(*receipt, sep='\n')
