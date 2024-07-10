from util.parser import get_globals
from util.dsha256 import dhash
from util.merkle_maker import *


def run(
        mr: str,
        tx_list: list[str],
        index: int
):
    print(mr, tx_list, index)
    i = 0

    # while True:
    while True:
        # i to 064x
        pred = format(i, '064x')
        merkle_root = calculate_merkle_root(tx_list, index, pred)
        if merkle_root == mr:
            return pred
        i += 1
        tx_list[index] = dhash(tx_list[index])

        if i % 100000 == 0:
            print(i, pred, merkle_root)


if __name__ == '__main__':
    mr, tx_list, index = get_globals()
    print(f"{mr=}")
    print(*tx_list, sep='\n')
    print(f"{index=}")
    res = run(mr, tx_list, index)
    print(f"{res=}")
