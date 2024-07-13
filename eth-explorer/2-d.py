from eth_hash.auto import (
    keccak,
)
from eth_typing import (
    Address,
)
from rlp import encode as rlp


# https://github.com/ethereum/py-evm/blob/d8df507e42c885ddeca2b64bbb8f10705f075d3e/eth/_utils/address.py#L20C1-L21C72
def _sol_1(address: Address, nonce: int) -> Address:
    trimmed_value = keccak(rlp([address, nonce]))[-20:]
    padded_value = trimmed_value.rjust(20, b"\x00")
    return Address(padded_value)


# https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1014.md#address-formula
def _sol_2(sender: Address, nonce: int) -> Address:
    # address_bytes = keccak(rlp.encode([sender, nonce]))[-20:]
    address_bytes = keccak(rlp([sender, nonce]))[12:]
    return Address(address_bytes)


def solve(deployer: str, nonce: int) -> Address:
    deployer_address = Address(bytes.fromhex(deployer))
    res = _sol_2(deployer_address, nonce)
    assert res == _sol_1(deployer_address, nonce)

    print(f"Deployer address: {deployer_address.hex()}")
    print(f"Nonce: {nonce}")
    print(f"Result: {res.hex()}")
    print("--------------------")

    return Address(res)


if __name__ == '__main__':
    deployer = 'B49bf876BE26435b6fae1Ef42C3c82c5867Fa149'
    contract_121 = Address(bytes.fromhex('4b4438eA9340f9dF6BBb13deb2129Ee8450b5F24'))

    assert solve(deployer, 121) == contract_121
    print(solve(deployer, 1337).hex())
