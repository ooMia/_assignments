import hashlib
import random

from Crypto.Util.number import *


def is_qr(v, p):
    return pow(v, (p - 1) // 2, p) == 1


def sqrt(v, p):
    assert p % 4 == 3
    assert is_qr(v, p)

    return pow(v, (p + 1) // 4, p)


def random_point(d, p):
    while True:
        x = random.randint(1, p - 1)
        y_square = (-x ** 2 - 1) * pow(d * x ** 2 - 1, -1, p)

        if is_qr(y_square, p):
            y = sqrt(y_square, p)
            return x, y


def is_on_curve(P, d, p):
    x, y = P
    return (-x * x + y * y) % p == (1 + d * x * x * y * y) % p


if __name__ == "__main__":
    while True:
        p = getStrongPrime(512)
        if p % 4 == 3:
            break

    while True:
        d = random.randint(2, p - 1)
        if not is_qr(d, p):
            break

    P = random_point(d, p)
    Q = random_point(d, p)

    from A3 import add, double

    P2Q2 = add(double(P, d, p), double(Q, d, p), d, p)
    P2Q2_ = double(add(P, Q, d, p), d, p)

    assert P2Q2 == P2Q2_
    assert is_on_curve(P2Q2, d, p)

    print(f"{p = }")
    print(f"{d = }")

    print(f"{P = }")
    print(f"{Q = }")

    x, y = P2Q2
    flag = hashlib.sha256(long_to_bytes(x) + long_to_bytes(y)).hexdigest()
    print("Flag is DH{" + flag + "}")
