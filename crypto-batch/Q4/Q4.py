import os
import random

from blspy import PrivateKey, BasicSchemeMPL, G1Element, G2Element, GTElement, PublicKeyMPL, SignatureMPL


def mult(k: int, G: PublicKeyMPL | SignatureMPL | GTElement) -> G2Element:
    """
    Multiply G-Element by scalar k
    Args:
        k: scalar
        G: PublicKeyMPL | SignatureMPL | GTElement
    Returns: k * G
    """

    if k == 1:
        return G

    T: G2Element = mult(k // 2, G)
    T = T + T
    if k % 2 == 1:
        T = T + G

    return T


def pow_gt(e: PublicKeyMPL | SignatureMPL | GTElement, k: int) -> GTElement:
    """
    Power of G-Element to scalar k
    Args:
        e: PublicKeyMPL | SignatureMPL | GTElement
        k: scalar
    Returns: e ** k
    """
    if k == 1:
        return e

    t: GTElement = pow_gt(e, k // 2)
    t = t * t
    if k % 2 == 1:
        t = t * e

    return t


def batch_verify(sigs: list[G2Element], msgs: list[bytes], coefs: list[int]) -> bool:
    """
    Batch verify signatures
    Notes:
        - LHS = sum(coef[i] * sig[i])
        - RHS = mul(pk.pair(msg[i]) ** coef[i])
    """
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


if __name__ == "__main__":
    sk: PrivateKey = PrivateKey.from_bytes(b"\x00" + os.urandom(31))
    pk: G1Element = sk.get_g1()

    print(f"{pk = }")

    msg1: bytes = b"upside"
    msg2: bytes = b"academy"
    msg3: bytes = b"best"

    sig1: G2Element = BasicSchemeMPL.sign(sk, msg1)
    sig2: G2Element = BasicSchemeMPL.sign(sk, msg2)
    sig3: G2Element = BasicSchemeMPL.sign(sk, msg3)

    print(f"{sig1 = }")
    print(f"{sig2 = }")
    print(f"{sig3 = }")

    assert batch_verify([sig1, sig2, sig3], [msg1, msg2, msg3], [3, 5, 7])

    coefs: list[int] = [random.randint(2, 2 ** (48 * 8)) for _ in range(6)]
    print(f"Coefs are: {coefs}")

    print("Give me your signatures!")
    # user_sig1 = G2Element.from_bytes(bytes.fromhex(input("sig1 > ")))
    # user_sig2 = G2Element.from_bytes(bytes.fromhex(input("sig2 > ")))
    # user_sig3 = G2Element.from_bytes(bytes.fromhex(input("sig3 > ")))

    from A4 import _solve, parse_input

    pk, sig1, sig2, sig3, ts1, ts2 = parse_input()
    user_sig1, user_sig2, user_sig3 = _solve(pk, sig1, sig2, sig3, coefs[:3], coefs[3:])

    if any(
            i == j for i in [sig1, sig2, sig3] for j in [user_sig1, user_sig2, user_sig3]
    ):
        print("NO HACK")
        exit(0)

    assert batch_verify(
        [user_sig1, user_sig2, user_sig3], [msg1, msg2, msg3], coefs[:3]
    )
    assert batch_verify(
        [user_sig1, user_sig2, user_sig3], [msg1, msg2, msg3], coefs[3:]
    )

    # with open("./flag", "r") as f:
    #     flag = f.read()
    #     print("Here is the flag:", flag)
    print(user_sig1, user_sig2, user_sig3, sep="\n")
    print("Good job!")
