import random

from merkle_maker import calculate_merkle_root
from util.dsha256 import dhash, btoh, sha256_


def run(
        mr: str,
        tx_list: list[str],
        index: int
):
    print(f"{mr=}")
    print(*tx_list, sep='\n')
    print(f"{index=}")

    while True:
        pred = btoh(sha256_(random.randbytes(2)))
        merkle_root = calculate_merkle_root(tx_list, index, pred)
        if merkle_root == mr:
            return pred
        tx_list[index] = dhash(tx_list[index])


if __name__ == '__main__':
    from util.parser import get_globals

    mr, tx_list, index = get_globals()
    res = run(mr, tx_list, index)
    print(f"{res=}")
