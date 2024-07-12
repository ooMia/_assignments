def get_inverse_in_circular_group(a, n) -> int:
    """
    a: element in the circular group modulo n
    n: modulus
    https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm#Example
    Returns the inverse of a in the circular group modulo n using the Extended Euclidean Algorithm.
    """

    # q: quotient (몫)
    # r: remainder (나머지)
    # s: coefficient of a (a의 계수)
    i, q, r, s = -1, 0, a, 1
    history = {}

    def log():
        nonlocal i, q, r, s
        i += 1
        history[i] = {"q": q, "r": r, "s": s}

    log()
    (q, r, s) = (0, n, 0)
    log()
    while r != 0:
        q = history[i - 1]["r"] // history[i]["r"]
        r = history[i - 1]["r"] - q * history[i]["r"]
        s = history[i - 1]["s"] - q * history[i]["s"]
        log()
    inverse = history[i - 1]["s"]
    assert (a * inverse) % n == 1

    def print_log():
        # print header to have 10 spaces for each value
        print(f"{'i':>2} {'q':>10} {'r':>10} {'s':>10}")
        print(f"{'-' * 40}")
        for k, v in history.items():
            v = [i for i in v.values()]
            print(f"{k:>2} {' '.join(f'{value:>10}' for value in v)}")

    print_log()
    return inverse


if __name__ == '__main__':
    print(get_inverse_in_circular_group(5, 37))
    print(get_inverse_in_circular_group(7653, 11200))
