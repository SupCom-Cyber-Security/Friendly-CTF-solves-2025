from functools import reduce
from binascii import hexlify

n = 122584705155240318506096954315788098857287510013471211255767087037145104765
c = 97751139831985916737101396826297056636739717782189373550258225442293878460
e = 65537

factors = [
    3,
    5,
    41,
    563,
    887,
    3953336221,
    100963734200067862974508853601922989321640538156533094011
]
prod = 1

for p in factors:
    prod *= p

print("Using factorization with", len(factors), "primes.")

phi_n = 1

for p in factors:
    phi_n *= (p - 1)


    d = pow(e, -1, phi_n)


m = pow(c, d, n)

def int_to_bytes(i):
    if i == 0:
        return b"\x00"
    length = (i.bit_length() + 7) // 8
    return i.to_bytes(length, 'big')
plain_bytes = int_to_bytes(m)





print("\nDecrypted integer m (dec):", m)


print("Decrypted (hex):", plain_bytes.hex())


print("Decrypted raw bytes:", plain_bytes)






