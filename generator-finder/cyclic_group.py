def multiplicative_group_of_modulus(p: int) -> set:
    from math import gcd
    return {x for x in range(1, p) if gcd(x, p) == 1}


def generators_of_multiplicative_group_of_modulus(p: int) -> set:
    _group = multiplicative_group_of_modulus(p)
    _generators = set()

    # Iterate through each element in the group
    for g in _group:
        # Generate a set of powers of g modulo p
        res = {pow(g, i, p) for i in range(1, p)}

        # Check if the size of the powers set is equal to the size of the group
        # If true, it means g is a generator of the group
        if len(res) == len(_group):
            assert res == _group
            _generators.add(g)
            # print(p, ":", g, res)

    return _generators


def solve(p: int) -> tuple[set, set]:
    return (multiplicative_group_of_modulus(p),
            generators_of_multiplicative_group_of_modulus(p))


if __name__ == '__main__':
    group = multiplicative_group_of_modulus
    assert group(6) == {1, 5}
    assert group(7) == {1, 2, 3, 4, 5, 6}
    assert group(8) == {1, 3, 5, 7}
    assert group(9) == {1, 2, 4, 5, 7, 8}
    assert group(10) == {1, 3, 7, 9}
    assert group(11) == {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}

    generators = generators_of_multiplicative_group_of_modulus
    assert generators(6) == {5}
    assert generators(7) == {3, 5}
    assert generators(8) == set()
    assert generators(9) == {2, 5}
    assert generators(10) == {3, 7}
    assert generators(11) == {2, 6, 7, 8}

    for i in range(5, 14):
        sol = solve(i)
        print(f"{i}:\t{sol[0]}")
        print("\t" + f"{"No generator" if len(sol[1]) < 1 else sol[1]}")
