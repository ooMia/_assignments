def _base_2_exp(n: int):
    return [i for i in range(0, n.bit_length()) if n & (1 << i)]


def solve_1(_base: int, _exp: int, _mod: int) -> int:
    res = 1
    for i in _base_2_exp(_exp)[::-1]:
        res *= pow(_base, 2 ** i, _mod)
        res %= _mod
        print(f"{i:2}: {res}")

    print("-" * 15)
    print(f"solve_1: {res}")
    return res


def solve_2(_base: int, _exp: int, _mod: int) -> int:
    res = 1

    def get_new_base_exp(_base, _exp, _mod):
        nonlocal res
        if _base == 1:
            return _base, 0
        if _exp % 2 == 1:
            _exp -= 1
            res = res * _base % _mod
            print(f"{res:5} | {_base:5}^{_exp + 1:5} ≡ {_base:5}^{_exp:5} * {_base} (mod {_mod})")
        new_base = _base ** 2 % _mod
        new_exp = _exp // 2
        print(f"{res:5} | {_base:5}^{_exp:5} ≡ {new_base:5}^{new_exp:5} \t\t (mod {_mod})")
        return new_base, new_exp

    while _exp > 0:
        _base, _exp = get_new_base_exp(_base, _exp, _mod)

    print("-" * 15)
    print(f"solve_2: {res}")
    return res


if __name__ == '__main__':
    base, exp, mod = 3233, 9517, 11413

    # calculate 3233^9517 ≡ x (mod 11413)
    # denote 9517 = 8,192 + 1024 + 256 + 32  +  8  +  4  +  1
    #             = 2^13  + 2^10 + 2^8 + 2^5 + 2^3 + 2^2 + 2^0
    a1 = solve_1(base, exp, mod)
    print("")

    # calculate 3233^9517 ≡ x (mod 11413)
    # start from 3233^2 ^ 11413
    # no update of res until exp is odd
    a2 = solve_2(base, exp, mod)
    assert a1 == a2
