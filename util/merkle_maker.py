from util.dsha256 import dhash, htob


def get_parent_of(idx: int) -> int:
    """get the index of the parent node of the given index"""
    return (idx - 1) // 2


def get_left_child_of(idx: int) -> int:
    """get the index of the left child node of the given index"""
    return idx * 2 + 1


def get_right_child_of(idx: int) -> int:
    """get the index of the right child node of the given index"""
    return idx * 2 + 2


def calculate_merkle_root(txs: list[str], idx: int, answer: str):
    txs[idx] = answer

    while len(txs) > 1:
        new_txs = []
        for i in range(0, len(txs), 2):
            try:
                h = dhash(txs[i], txs[i + 1])
            except IndexError:
                h = dhash(txs[i])
            new_txs.append(h)
        txs = new_txs
    return txs[0]


if __name__ == '__main__':
    from util.parser import get_globals
    mr, tx_list, index = get_globals()
    res = calculate_merkle_root(tx_list, 0, "adcc7b631011debe749ee4f97efaa4fe55d321e2153e460ae0b798369d033b7f")
    print(mr == res)
