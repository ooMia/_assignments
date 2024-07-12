def extended_euclidean(a, b) -> tuple:
    """
    https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm#Example
    Solve the linear equation:
        ax + by = g where g = gcd(a, b)
    Return the solution x, y and g
    """

    # q: quotient (몫)
    # r: remainder (나머지)
    # s: coefficient of a (a의 계수)
    # t: coefficient of b (b의 계수)
    i, q, r, s, t = -1, 0, a, 1, 0
    history = {}

    def log():
        nonlocal i, q, r, s, t
        i += 1
        history[i] = {"q": q, "r": r, "s": s, "t": t}

    log()
    (q, r, s, t) = (0, b, 0, 1)
    log()
    while r != 0:
        q = history[i - 1]["r"] // history[i]["r"]
        r = history[i - 1]["r"] - q * history[i]["r"]
        s = history[i - 1]["s"] - q * history[i]["s"]
        t = history[i - 1]["t"] - q * history[i]["t"]
        log()
    x, y = history[i]["s"], history[i]["t"]
    g = history[i - 1]["r"]

    def print_log():
        # print header to have 10 spaces for each value
        print(f"{'i':>2} {'q':>10} {'r':>10} {'s':>10} {'t':>10}")
        print(f"{'-' * 50}")
        for k, v in history.items():
            v = [i for i in v.values()]
            print(f"{k:>2} {' '.join(f'{value:>10}' for value in v)}")

    print_log()
    return x, y, g


if __name__ == '__main__':
    a, b = 12345, 123
    x, y, g = extended_euclidean(a, b)
    print(x, y, g)  # (-41, 4115, 3)

    a, b = 240, 46
    x, y, g = extended_euclidean(a, b)
    print(x, y, g)  # (23, -120, 2)
