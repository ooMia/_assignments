import random
import re
from math import gcd

from blspy import G1Element, G2Element


def parse_input() -> tuple[G1Element, G2Element, G2Element, G2Element, list[int]]:
    with open("input.txt", "r") as f:
        # pk = <G1Element 0xxxxx>
        match = re.search(r"<G1Element ([0-9a-fA-F]+)>", f.readline().strip())
        pk = G1Element.from_bytes(bytes.fromhex(match.group(1)))

        # sig2 = <G2Element 0xxxxx>
        sigs = []
        for _ in range(3):
            match = re.search(r"<G2Element ([0-9a-fA-F]+)>", f.readline().strip())
            s = G2Element.from_bytes(bytes.fromhex(match.group(1)))
            sigs.append(s)

        # Coefs are: [1, 2, 3, 4, 5, 6]
        line = f.readline().strip()
        ts = list(map(int, re.findall(r"\d+", line)))

        return pk, sigs[0], sigs[1], sigs[2], ts


def sum_product(a, b, m=None):
    if m is None:
        return sum(ai * bi for ai, bi in zip(a, b))
    res = 0
    for ai, bi in zip(a, b):
        res += ((ai % m) * (bi % m)) % m
        res %= m
    return res


def _solve(
    p: int,  # strong prime
    y: int,  # public key
    sig1: tuple[int, int],  # signature 1 (r, s)
    sig2: tuple[int, int],  # signature 2 (r, s)
    sig3: tuple[int, int],  # signature 3 (r, s)
    ts1: list[int],  # list of first 3 random coefficients
    ts2: list[int],  # list of last 3 random coefficients
) -> list[int]:  # new signatures [r1, s1, r2, s2, r3, s3]

    def find_intersection_point(A, B, C, D, E, F, G, H, p):
        # 최대공약수 g 계산
        g_A = gcd(A, gcd(B, C))
        g_E = gcd(E, gcd(F, G))
        g = gcd(g_A, g_E)

        # g로 나눈 값을 사용: 확장된 베주 항등식
        A, B, C, D = A // g, B // g, C // g, D // g
        E, F, G, H = E // g, F // g, G // g, H // g

        # x0, y0, z0 초기값 설정
        x0, y0, z0 = sig1[1], sig2[1], sig3[1]
        assert A * x0 + B * y0 + C * z0 == D

        # 방향 벡터 구하기
        x_dir = B * G - C * F
        y_dir = C * E - A * G
        z_dir = A * F - B * E

        print(f"{x0=}, {y0=}, {z0=}")
        print(f"{x_dir=}, {y_dir=}, {z_dir=}")

        while True:
            t = random.randint(2, 1000)
            x = addmod(p - 1, x0, mulmod(p - 1, t, x_dir))
            y = addmod(p - 1, y0, mulmod(p - 1, t, y_dir))
            z = addmod(p - 1, z0, mulmod(p - 1, t, z_dir))

            # 각 좌표가 mod (p-1) 이후에도 교선에 존재하는지 검증
            if (A * x + B * y + C * z) % (p - 1) == D % (p - 1):
                if (E * x + F * y + G * z) % (p - 1) == H % (p - 1):
                    return [x, y, z]

    s1, s2, s3 = sig1[1], sig2[1], sig3[1]
    k1 = sum_product(ts1, [s1, s2, s3])
    k2 = sum_product(ts2, [s1, s2, s3])
    res = find_intersection_point(*ts1, k1, *ts2, k2, p)
    if res is None:
        raise ValueError("No intersection point found")
    return [sig1[0], res[0], sig2[0], res[1], sig3[0], res[2]]


def mulmod(m, *numbers):
    if not numbers:
        raise ValueError("No numbers to multiply")
    res = 1
    for n in numbers:
        res *= n
        res %= m
    return res


def addmod(m, *numbers):
    if not numbers:
        raise ValueError("No numbers to add")
    res = 0
    for n in numbers:
        res += n
        res %= m
    return res


if __name__ == "__main__":
    g = 2
    p, y, [sig1, sig2, sig3], ts1, ts2 = parse_input()
    print(f"{p=}")

    # print(f"{y=}")
    # print(f"{sig1=}")
    # print(f"{sig2=}")
    # print(f"{sig3=}")
    # print(f"{ts1=}")
    # print(f"{ts2=}")

    # Extended Bezout's identity
    # d1 = gcd(ts1[0], ts1[1], ts1[2])
    # d2 = gcd(ts2[0], ts2[1], ts2[2])
    # print(f"{d1 = } {d2 = }")
    #
    # k1 = sum_product(ts1, [sig1[1], sig2[1], sig3[1]], d2)
    # k2 = sum_product(ts2, [sig1[1], sig2[1], sig3[1]], d1)
    # print(f"{k1 = } {k2 = }")
    #
    # assert k1 % d1 == 0
    # assert k2 % d2 == 0
    # print(f"{ts1 = } {ts2 = }")
    # print(f"{k1 % (p-1) = } {k2 % (p-1) = }")
    #
    # s1, s2, s3 = sig1[1], sig2[1], sig3[1]
    # k0 = 3 * s1 + 5 * s2 + 7 * s3
    #
    # # Fermat's little theorem
    # assert pow(g, k0, p) == pow(g, k0 % (p - 1), p)
    # assert pow(g, k1, p) == pow(g, k1 % (p - 1), p)
    # assert pow(g, k2, p) == pow(g, k2 % (p - 1), p)

    res = _solve(p, y, sig1, sig2, sig3, ts1, ts2)
    print(*res, sep="\n")
