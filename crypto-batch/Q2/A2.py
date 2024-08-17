import re


def parse_input() -> tuple[int, int, list[tuple[int, int]], list[int], list[int]]:
    with open('input.txt', 'r') as f:
        p = int(f.readline().strip().split()[-1])
        y = int(f.readline().strip().split()[-1])

        # sig1 = (r, s)
        sigs = []
        sig_pattern = re.compile(r'\((\d+), (\d+)\)')
        for _ in range(3):
            line = f.readline().strip().split(" = ")[-1]
            match = sig_pattern.search(line)
            if match:
                r = int(match.group(1))
                s = int(match.group(2))
                sigs.append((r, s))

        # Coefs are: [1, 2, 3, 4, 5, 6]
        line = f.readline().strip()
        ts = list(map(int, re.findall(r'\d+', line)))

        return p, y, sigs, ts[:3], ts[3:]


def solve(
        p: int,
        y: int,
        sig1: tuple[int, int],
        sig2: tuple[int, int],
        sig3: tuple[int, int],
        coefs: list[int]
) -> tuple[int, int, int, int, int, int]:
    return 0, 0, 0, 0, 0, 0


if __name__ == '__main__':
    p, y, [sig1, sig2, sig3], ts1, ts2 = parse_input()
    print(f"{p=}")
    print(f"{y=}")
    print(f"{sig1=}")
    print(f"{sig2=}")
    print(f"{sig3=}")
    print(f"{ts1=}")
    print(f"{ts2=}")
