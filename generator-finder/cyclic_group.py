def multiplicative_group_of_modulus(n: int) -> set:
    from math import gcd
    return {x for x in range(1, n) if gcd(x, n) == 1}


def generators_of_multiplicative_group_of_modulus(n: int) -> set:
    _group = multiplicative_group_of_modulus(n)
    _generators = set()

    # Iterate through each element in the group
    for g in _group:
        # Generate a set of powers of g modulo p
        res = {pow(g, i, n) for i in range(1, n)}

        # Check if the size of the powers set is equal to the size of the group
        # If true, it means g is a generator of the group
        if len(res) == len(_group):
            assert res == _group
            _generators.add(g)
            for g in _group:
                assert g in res
            # print(p, ":", g, res)

    return _generators


def validation(n: int):
    _group = multiplicative_group_of_modulus(n)
    _generators = generators_of_multiplicative_group_of_modulus(n)

    print(f"n{n}\t\t", end="")
    print(*range(len(_group) + 1), sep="\t", end="\t")
    print(_group)
    print("-" * 50)
    # for g in _generators:
    for g in _group:
        print(f"g{g}\t", end="\t")
        print(*[pow(g, x, n) for x in range(len(_group) + 1)], sep="\t", end="\t")
        res = {pow(g, i, n) for i in range(1, n)}
        print(res)
        if len(res) == len(_group):
            assert res == _group, f"{n}: {res} is not equal to {_group}"


def solve(p: int) -> tuple[set, set]:
    return (multiplicative_group_of_modulus(p),
            generators_of_multiplicative_group_of_modulus(p))


if __name__ == '__main__':
    group = multiplicative_group_of_modulus
    assert group(5) == {1, 2, 3, 4}
    assert group(6) == {1, 5}
    assert group(7) == {1, 2, 3, 4, 5, 6}
    assert group(8) == {1, 3, 5, 7}
    assert group(9) == {1, 2, 4, 5, 7, 8}
    assert group(10) == {1, 3, 7, 9}
    assert group(11) == {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}

    generators = generators_of_multiplicative_group_of_modulus
    assert generators(5) == {2, 3}
    assert generators(6) == {5}
    assert generators(7) == {3, 5}
    assert generators(8) == set()
    assert generators(9) == {2, 5}
    assert generators(10) == {3, 7}
    assert generators(11) == {2, 6, 7, 8}

    for i in range(5, 20):
        sol = solve(i)
        print(f"{i}:\t{sol[0]}")
        print("\t" + f"{"No generator" if len(sol[1]) < 1 else sol[1]}")
    print()

    for i in range(5, 30):
        validation(i)
        print()