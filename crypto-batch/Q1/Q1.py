import hashlib
import random

from Crypto.Util.number import bytes_to_long, getStrongPrime

p = getStrongPrime(512)
g = 2
x = random.randint(2, p - 2)  # private key
y = pow(g, -x, p)  # public key

print(f"{p = }")
print(f"{y = }")


def sign(m, x, p):
    k = random.randint(2, p - 2)
    r = pow(g, k, p)

    e = bytes_to_long(hashlib.sha256(str(r).encode() + m.encode()).digest())
    s = (k + x * e) % (p - 1)
    return r, s  # r: ephemeral public key, s: signature


def verify(sig, m, y, p):
    r, s = sig
    e = bytes_to_long(hashlib.sha256(str(r).encode() + m.encode()).digest())

    return (pow(g, s, p) * pow(y, e, p) % p) == r


sig1 = sign('upside', x, p)
assert verify(sig1, 'upside', y, p)

sig2 = sign('academy', x, p)
assert verify(sig2, 'academy', y, p)

print(f"{sig1 = }")
print(f"{sig2 = }")


def batch_verify(sig1, sig2, m1, m2, t1, t2, y, p):
    r1, s1 = sig1
    r2, s2 = sig2

    e1 = bytes_to_long(hashlib.sha256(str(r1).encode() + m1.encode()).digest())
    e2 = bytes_to_long(hashlib.sha256(str(r2).encode() + m2.encode()).digest())

    l = pow(g, t1 * s1 + t2 * s2, p)
    l = l * pow(y, e1 * t1, p) * pow(y, e2 * t2, p) % p

    r = pow(r1, t1, p) * pow(r2, t2, p) % p

    return l == r


assert batch_verify(sig1, sig2, 'upside', 'academy', 3, 5, y, p)

print("Give me your signatures!")
r1 = int(input('r1 > ')) % p
s1 = int(input('s1 > ')) % (p - 1)
r2 = int(input('r2 > ')) % p
s2 = int(input('s2 > ')) % (p - 1)

if (r1, s1) in [sig1, sig2] or (r2, s2) in [sig1, sig2]:
    print("NO HACK")
    exit(0)

# assert batch_verify((r1, s1), (r2, s2), 'upside', 'academy', 3, 5, y, p)

with open('./flag', 'r') as f:
    flag = f.read()
    print("Here is the flag:", flag)
