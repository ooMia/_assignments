from hashlib import sha256


# https://dreamhack.io/forum/qna/1515/
#
# (1)
# sha256() (X)
# sha256(sha256()) (O)
#
# (2)
# string.encode() => b'aa' (X)
# bytes.fromhex() => b'\xaa' (O)
#
# (3)
#      Python Big-endian   <-->  BitCoin Little-endian
#  bytes.fromhex & [::-1]  <-->  [::-1] & bytes.hex()


def htob(hex: str) -> bytes:
    """
    Convert hex strings to bytes in little endian format.
    Adjusted for little-endian system compatibility.
    """
    # Convert hex to bytes then reverse for little-endian
    return bytes.fromhex(hex)[::-1]


def btoh(byte: bytes) -> str:
    """
    Convert bytes to hex strings in big endian format.
    Adjusted for little-endian system compatibility.
    """
    # Reverse bytes for little-endian then convert to hex
    return byte[::-1].hex()


def sha256_(bi: bytes) -> bytes:
    return sha256(bi).digest()


def dhash(bi_1: str, bi_2: str = None) -> str:
    # https://github.com/bitcoin/bitcoin/blob/9adebe145557ef410964dd48a02f3d239f488cd0/src/consensus/merkle.cpp#L13
    if bi_2 is None:
        bi_2 = bi_1
    return btoh(sha256_(sha256_(htob(bi_1) + htob(bi_2))))


if __name__ == '__main__':
    def htob_2(x):
        return int(x, 16).to_bytes(length=32, byteorder='little')


    H_a = 'adcc7b631011debe749ee4f97efaa4fe55d321e2153e460ae0b798369d033b7f'
    H_b = 'a8f0f38acc57d76e4dc1e549d20599da6339fe7269b4b4a838ab733e36e4aacb'
    expect = '0289c815b5994037762d54302909bc643cf76efcd9b77714a1e30c1c16f4b8ac'
    assert expect == dhash(H_a, H_b)
    assert htob(H_a) == htob_2(H_a)
    pass
