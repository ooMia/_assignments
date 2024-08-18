import hashlib
import random
from math import gcd

from Crypto.Util.number import getStrongPrime, bytes_to_long
from A2 import sum_product


def sign(m, x, p):
    k = random.randint(2, p - 2)
    r = pow(g, k, p)

    e = bytes_to_long(hashlib.sha256(str(r).encode() + m.encode()).digest())
    s = (k + x * e) % (p - 1)
    return r, s


def verify(sig, m, y, p):
    r, s = sig
    e = bytes_to_long(hashlib.sha256(str(r).encode() + m.encode()).digest())

    return (pow(g, s, p) * pow(y, e, p) % p) == r


def batch_verify(sigs, ms, ts, y, p):
    es = [
        bytes_to_long(hashlib.sha256(str(ri).encode() + mi.encode()).digest())
        for (ri, _), mi in zip(sigs, ms)
    ]

    l, r = 1, 1
    for i in range(len(sigs)):
        l *= pow(g, ts[i] * sigs[i][1], p)
        l *= pow(y, es[i] * ts[i], p)
        l %= p

        r *= pow(sigs[i][0], ts[i], p)
        r %= p

    return l == r


if __name__ == "__main__":
    p = getStrongPrime(512)
    g = 2
    x = random.randint(2, p - 2)
    y = pow(g, -x, p)

    print(f"{p = }")
    print(f"{y = }")

    sig1 = sign("upside", x, p)
    assert verify(sig1, "upside", y, p)

    sig2 = sign("academy", x, p)
    assert verify(sig2, "academy", y, p)

    sig3 = sign("best", x, p)
    assert verify(sig3, "best", y, p)

    print(f"{sig1 = }")
    print(f"{sig2 = }")
    print(f"{sig3 = }")

    assert batch_verify(
        [sig1, sig2, sig3], ["upside", "academy", "best"], [3, 5, 7], y, p
    )

    coefs = [random.randint(2, p - 2) for _ in range(6)]
    print(f"Coefs are: {coefs}")

    # Extended Bezout's identity
    ts1 = coefs[0], coefs[1], coefs[2]
    ts2 = coefs[3], coefs[4], coefs[5]
    d1 = gcd(*ts1)
    d2 = gcd(*ts2)
    print(f"{d1 = } {d2 = }")

    k1 = sum_product(ts1, [sig1[1], sig2[1], sig3[1]], d2)
    k2 = sum_product(ts2, [sig1[1], sig2[1], sig3[1]], d1)
    print(f"{k1 = } {k2 = }")

    from A2 import _solve, sum_product

    print("Give me your signatures!")
    r1, s1, r2, s2, r3, s3 = _solve(p, y, sig1, sig2, sig3, coefs[:3], coefs[3:])
    r1 %= p
    r2 %= p
    r3 %= p
    s1 %= p - 1
    s2 %= p - 1
    s3 %= p - 1

    if any((ri, si) in [sig1, sig2, sig3] for ri, si in [(r1, s1), (r2, s2), (r3, s3)]):
        print("NO HACK")
        exit(0)

    assert batch_verify(
        [(r1, s1), (r2, s2), (r3, s3)], ["upside", "academy", "best"], coefs[:3], y, p
    )
    assert batch_verify(
        [(r1, s1), (r2, s2), (r3, s3)], ["upside", "academy", "best"], coefs[3:], y, p
    )

    print(r1, s1, r2, s2, r3, s3, sep="\n")

    # with open('./flag', 'r') as f:
    #     flag = f.read()
    #     print("Here is the flag:", flag)
