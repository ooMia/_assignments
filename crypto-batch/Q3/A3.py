import re


def parse_output() -> tuple[int, int, tuple[int, int], tuple[int, int]]:
    with open("output.txt", "r") as f:
        p = int(f.readline().strip().split()[-1])
        d = int(f.readline().strip().split()[-1])

        # P = (x, y)
        match = re.search(r"\((\d+), (\d+)\)", f.readline().strip())
        P = (int(match.group(1)), int(match.group(2)))

        # P = (x, y)
        match = re.search(r"\((\d+), (\d+)\)", f.readline().strip())
        Q = (int(match.group(1)), int(match.group(2)))

        return p, d, P, Q


def summod(p: int, *nums: int):
    res = 0
    for n in nums:
        res = (res + n) % p
    return res


def mulmod(p: int, *nums: int):
    res = 1
    for n in nums:
        res = (res * n) % p
    return res


def add(P, Q, d, p):
    """
    References:
        https://en.wikipedia.org/wiki/Twisted_Edwards_curve#Addition_on_twisted_Edwards_curves
    """
    a = -1
    x1, y1 = P
    x2, y2 = Q
    mul = lambda *n: mulmod(p, *n)
    add = lambda *n: summod(p, *n)

    x3 = add(mul(x1, y2), mul(y1, x2))
    x3 *= pow(add(1, mul(d, x1, x2, y1, y2)), -1, p)

    y3 = add(mul(y1, y2), mul(-a, x1, x2))
    y3 *= pow(add(1, mul(-d, x1, x2, y1, y2)), -1, p)

    return x3 % p, y3 % p


def double(P, d, p):
    """
    References:
        https://en.wikipedia.org/wiki/Twisted_Edwards_curve#Doubling_on_twisted_Edwards_curves
    """
    a = -1
    x1, y1 = P
    mul = lambda *n: mulmod(p, *n)
    add = lambda *n: summod(p, *n)

    x3 = mul(2, x1, y1)
    x3 *= pow(add(mul(a, mul(x1, x1)), mul(y1, y1)), -1, p)

    y3 = add(mul(y1, y1), mul(-a, x1, x1))
    y3 *= pow(add(2, mul(-a, x1, x1), mul(-y1, y1)), -1, p)

    return x3 % p, y3 % p


if __name__ == "__main__":
    import hashlib
    from Crypto.Util.number import long_to_bytes
    from Q3 import is_on_curve

    """
    Notes:
        Twisted Edwards Curve Practice
        Implement add and double functions
        Equation: is a * x^2 + y^2 = 1 + d*x^2*y^2 where a = -1
    """
    a = -1
    p, d, P, Q = parse_output()
    sum_2p_2q = add(double(P, d, p), double(Q, d, p), d, p)
    mul2_sum_pq = double(add(P, Q, d, p), d, p)

    print(f"{sum_2p_2q = }")
    print(f"{mul2_sum_pq = }")

    assert sum_2p_2q == mul2_sum_pq
    assert is_on_curve(sum_2p_2q, d, p)

    x, y = sum_2p_2q
    flag = hashlib.sha256(long_to_bytes(x) + long_to_bytes(y)).hexdigest()
    print("Flag is DH{" + flag + "}")
