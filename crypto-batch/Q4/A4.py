import re

from blspy import G1Element, G2Element


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
) -> list[int]:  # new signatures [s1, s2, s3]
    msg1: bytes = b"upside"
    msg2: bytes = b"academy"
    msg3: bytes = b"best"

    res = [sig1, sig2, sig3]
    return res


if __name__ == "__main__":
    pk, sig1, sig2, sig3, ts1, ts2 = parse_input()
    res = _solve(pk, sig1, sig2, sig3, ts1, ts2)
    print(*res, sep="\n")
