import random
from hashlib import sha256
from util.parser import get_globals
from util.dsha256 import dhash
from merkle_maker import calculate_merkle_root


def run(
        mr: str,
        tx_list: list[str],
        index: int
):
    print(mr, tx_list, index)

    while True:
        pred = sha256(random.randbytes(2)).digest()[::-1].hex()
        merkle_root = calculate_merkle_root(tx_list, index, pred)
        if merkle_root == mr:
            return pred
        tx_list[index] = dhash(tx_list[index])


if __name__ == '__main__':
    mr, tx_list, index = get_globals()
    print(f"{mr=}")
    print(*tx_list, sep='\n')
    print(f"{index=}")
    res = run(mr, tx_list, index)
    print(f"{res=}")
