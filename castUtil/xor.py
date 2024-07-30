from eth_hash.auto import (
    keccak,
)

target = "77aeec0b38e07e77e0fceaee2742275c84ac2fc0026da95abfb692a7b934a280"
caller = "4262Aa56B97f776C075883b6077719ca3B997023"


def hex_hex_xor(h1: str, h2: str) -> str:
    return hex(int(h1, 16) ^ int(h2, 16))[2:]


def do_iter(t: str) -> str:
    friends = ["5506b53ae79b3f85bc16ee8f265bd06dfb862677102f9f99f66628f130717331",
               "345b666897fc960d9bda0fab6a75830bb2dd4dda3f4804731ac4ff7722c7dcd",
               "333c86e14b3dbbb36563c1da6120387d418af2250faf48da26536a9111acc717",
               "7a9c571c22a679da5b82394f8ead31cf567a930e6827e9564c50bd722114afc7", ]
    for f in friends:
        t = hex_hex_xor(t, f)
    return t


def do_iter_reverse(t: str) -> str:
    friends = ["5506b53ae79b3f85bc16ee8f265bd06dfb862677102f9f99f66628f130717331",
               "345b666897fc960d9bda0fab6a75830bb2dd4dda3f4804731ac4ff7722c7dcd",
               "333c86e14b3dbbb36563c1da6120387d418af2250faf48da26536a9111acc717",
               "7a9c571c22a679da5b82394f8ead31cf567a930e6827e9564c50bd722114afc7", ]
    for f in friends[::-1]:
        t = hex_hex_xor(t, f)
    return t


if __name__ == "__main__":
    _in = target
    for _ in range(255):
        _in = do_iter_reverse(_in)
    print(_in)

    # zero padding
    a = caller.zfill(64)
    print(a)

    print(keccak(bytes.fromhex(a)).hex())
