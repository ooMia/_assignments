from eth_hash.auto import (
    keccak,
)

debug = False


def keccak_int(_slot: int) -> str:
    # Convert the number to big endian format
    big_endian_bytes = _slot.to_bytes(32, 'big')
    if debug:
        print(f"big_endian_bytes: {big_endian_bytes}")
    return keccak(big_endian_bytes).hex()


def keccak_mapping(_key: bytes or str or int, _slot: bytes or str or int) -> bytes:
    if isinstance(_key, int):
        y = _key.to_bytes(32, 'big')
    elif isinstance(_key, str):
        y = bytes(_key, 'utf-8')
    elif isinstance(_key, bytes):
        y = _key
    else:
        raise ValueError("Invalid key type")

    if isinstance(_slot, int):
        x = _slot.to_bytes(32, 'big')
    elif isinstance(_slot, str):
        x = bytes(_slot, 'utf-8')
    elif isinstance(_slot, bytes):
        x = _slot
    else:
        raise ValueError("Invalid key type")

    big_endian_bytes = y + x
    if debug:
        print(f"big_endian_bytes: {big_endian_bytes}")
    return keccak(big_endian_bytes)


if __name__ == "__main__":
    number = 1
    s1 = keccak_mapping(0, 0)
    s2 = keccak_mapping(s1, 0)
    print(s2)
