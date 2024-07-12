def solve_1():
    # calculate 3233^9517 ≡ x (mod 11413)
    # denote 9517 = 8,192 + 1024 + 256 + 32  +  8  +  4  +  1
    #             = 2^13  + 2^10 + 2^8 + 2^5 + 2^3 + 2^2 + 2^0

    res = 1
    for i in [13, 10, 8, 5, 3, 2, 0]:
        res *= pow(3233, 2 ** i, 11413)
        res %= 11413
        print(f"{i:2}: {res}")

    print("-" * 10)
    print(f"solve_1: {res}")


def solve_2():
    # calculate 3233^9517 ≡ x (mod 11413)
    # start from 3233^2 ^ 11413
    # no update of res until exp is odd
    res = 1
    _base = 3233
    _exp = 9517
    _mod = 11413

    def get_new_base_exp(base, exp, mod):
        if base == 1:
            return base, 0
        if exp % 2 == 1:
            nonlocal res
            exp -= 1
            res = res * base % mod
            print(f"{res:5} | {base:5}^{exp + 1:5} ≡ {base:5}^{exp:5} * {base} (mod {mod})")
        new_base = base ** 2 % mod
        new_exp = exp // 2
        print(f"{res:5} | {base:5}^{exp:5} ≡ {new_base:5}^{new_exp:5} \t\t (mod {mod})")
        return new_base, new_exp

    while _exp > 0:
        _base, _exp = get_new_base_exp(_base, _exp, _mod)

    print("-" * 10)
    print(f"solve_2: {res}")


if __name__ == '__main__':
    solve_1()
    print("")
    solve_2()
