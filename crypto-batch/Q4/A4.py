import re

from blspy import G1Element, G2Element, GTElement, BasicSchemeMPL

from Q4 import mult, pow_gt


def parse_input() -> tuple[G1Element, G2Element, G2Element, G2Element, list[int], list[int]]:
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

        return pk, sigs[0], sigs[1], sigs[2], ts[:3], ts[3:]


def _solve(
        pk: G1Element,  # public key
        sig1: G2Element,  # signature 1
        sig2: G2Element,  # signature 2
        sig3: G2Element,  # signature 3
        ts1: list[int],  # list of first 3 random coefficients
        ts2: list[int],  # list of last 3 random coefficients
) -> list[G2Element]:  # new signatures [s1, s2, s3]
    sigs = [sig1, sig2, sig3]

    def calc_k(sigs: list[G2Element], coefs: list[int]) -> G2Element:
        S: G2Element = None
        for sig, coef in zip(sigs, coefs):
            if S is None:
                S = mult(coef, sig)
            else:
                S = S + mult(coef, sig)
        return S

    def find_intersection_point(
            A: int, B: int, C: int, D: G2Element,
            E: int, F: int, G: int, H: G2Element
    ) -> list[G2Element]:
        """
        Notes:
            A*x + B*y + C*z = D
            E*x + F*y + G*z = H
            where
                A, B, C, E, F, G are known integers
                D, H are known G2Elements
                x, y, z are unknown G2Elements to find
        Returns:
            [x, y, z] if found
            None otherwise
        """

        # x0, y0, z0 초기값 설정
        x0: G2Element = sigs[0]
        y0: G2Element = sigs[1]
        z0: G2Element = sigs[2]
        assert mult(A, x0) + mult(B, y0) + mult(C, z0) == D
        assert mult(E, x0) + mult(F, y0) + mult(G, z0) == H

        # 방향 벡터 구하기
        x_dir: int = B * G - C * F
        y_dir: int = C * E - A * G
        z_dir: int = A * F - B * E

        # https://neuromancer.sk/std/bls/BLS12-381
        # Order n of the generator point
        # prevent maximum recursion depth exceeded error
        # order: int = 52435875175126190479447740508185965837690552500527637822603658699938581184513
        order_n = bytes.fromhex("73EDA753299D7D483339D80809A1D80553BDA402FFFE5BFEFFFFFFFF00000001")
        order_n = int.from_bytes(order_n, "big")
        x_dir %= order_n
        y_dir %= order_n
        z_dir %= order_n

        t: G2Element = G2Element.generator()
        x: G2Element = x0 + mult(x_dir, t)
        y: G2Element = y0 + mult(y_dir, t)
        z: G2Element = z0 + mult(z_dir, t)

        # 새롭게 구한 sigs가 교선에 존재하는지 검증
        if calc_k([x, y, z], [A, B, C]) == D:
            if calc_k([x, y, z], [E, F, G]) == H:
                assert not any(i == j for i in [sig1, sig2, sig3] for j in [x, y, z])
                return [x, y, z]

    k1 = calc_k(sigs, ts1)
    k2 = calc_k(sigs, ts2)
    new_sigs = find_intersection_point(*ts1, k1, *ts2, k2)
    if new_sigs is None:
        raise ValueError("No intersection point found")

    return new_sigs


def verify(sig1, sig2, sig3, ts1, ts2, pk):
    msg1, msg2, msg3 = b"upside", b"academy", b"best"

    def batch_verify(sigs: list[G2Element], msgs: list[bytes], coefs: list[int], pk: G1Element) -> bool:
        S: G2Element = None
        for sig, coef in zip(sigs, coefs):
            if S is None:
                S = mult(coef, sig)
            else:
                S = S + mult(coef, sig)
        L: GTElement = S.pair(G1Element.generator())

        R: GTElement = None
        for msg, coef in zip(msgs, coefs):
            if R is None:
                R = pow_gt(pk.pair(BasicSchemeMPL.g2_from_message(msg)), coef)
            else:
                R = R * pow_gt(pk.pair(BasicSchemeMPL.g2_from_message(msg)), coef)

        return L == R

    assert batch_verify([sig1, sig2, sig3], [msg1, msg2, msg3], ts1, pk)
    assert batch_verify([sig1, sig2, sig3], [msg1, msg2, msg3], ts2, pk)


if __name__ == "__main__":
    """
    Notes:
        Field extension
            - Embedding degree: 12
            - Degree of field extension: 12
        The basic equation of the BLS12-381 curve is y^2 = x^3 + 4
        The curve is defined over the finite field F_p where p = 2^381 - 3
        The generator point is G = (1, 2)
        The order of the generator point is n = 52435875175126190479447740508185965837690552500527637822603658699938581184513
    References:
        - [BLS12-381 For The Rest Of Us](https://hackmd.io/@benjaminion/bls12-381)
        - [Pairings for beginners](https://shorturl.at/ejpUG)
        - [Standard curve database](https://neuromancer.sk/std/bls/BLS12-381)
    """
    print("Parsing input...")
    pk, sig1, sig2, sig3, ts1, ts2 = parse_input()
    print(pk, sig1, sig2, sig3, ts1, ts2, sep="\n", end="\n\n")
    user_sig1, user_sig2, user_sig3 = _solve(pk, sig1, sig2, sig3, ts1, ts2)
    verify(user_sig1, user_sig2, user_sig3, ts1, ts2, pk)
    print("New signatures:", user_sig1, user_sig2, user_sig3, sep="\n")

    # 성질 정리
    # 각각 G1, G2에 존재하는 원소 X, Y와 Z에 대해
    # (X+Y).pair(Z) = X.pair(Z) * Y.pair(Z)
    assert (pk + G1Element.generator()).pair(sig1) == pk.pair(sig1) * G1Element.generator().pair(sig1)

    # 각각 G1, G2에 존재하는 원소 X 와 Y, Z에 대해
    # X.pair(Y+Z) = X.pair(Y) * X.pair(Z)
    assert pk.pair(sig1 + sig2) == pk.pair(sig1) * pk.pair(sig2)

    # 임의의 scalar a, b에 대해 (a * pk).pair(b * sig1)
    a, b = 2, 3
    k = mult(2, pk).pair(mult(3, sig1))  # (2 * pk).pair(3 * sig1)
    assert k == mult(3, pk).pair(mult(2, sig1))  # (3 * pk).pair(2 * sig1)
    assert k == pow_gt(mult(3, pk).pair(sig1), 2)  # (3 * pk).pair(sig1) ** 2
    assert k == pow_gt(pk.pair(sig1), 3 * 2)  # pk.pair(sig1) ** (3 * 2)
