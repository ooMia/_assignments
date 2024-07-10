from util.dsha256 import dhash


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
    res = calculate_merkle_root(tx_list, 0, "5f37fe4ddeb27c2fd2cf58af6409f85f5d2b7437ab0ee006be46809040e648a0")
    print(mr == res)
