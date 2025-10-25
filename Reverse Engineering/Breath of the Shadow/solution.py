def rol8(v, s):
    s &= 7
    return ((v << s) | (v >> ((8 - s) & 7))) & 0xFF

def runtime_key(idx):
    s = 0xDEADBEEF
    rounds = 3 + (idx % 5)
    for r in range(rounds):
        s = (s * 1664525 + 1013904223) & 0xFFFFFFFF
        s ^= ((s >> (r + 1)) + idx) & 0xFFFFFFFF
        s = (s + ((s & 0xFF) * (r + 7))) & 0xFFFFFFFF
    shift = (idx % 3) * 8
    return (s >> shift) & 0xFF

def decode(encoded_hex: str):
    if len(encoded_hex) % 2 != 0:
        raise ValueError("encoded hex length must be even")
    enc_bytes = bytes.fromhex(encoded_hex)
    n = len(enc_bytes)

    obf = [0] * n
    for i in range(n):
        b = enc_bytes[i]
        shown = rol8(b, i & 7)
        k = runtime_key(i)
 
        tmp = shown ^ k
        offset = (i * 13) & 0xFF
        x = (tmp - offset) & 0xFF
        obf[i] = x

    flag_bytes = bytes((obf[i] - 0x0d) & 0xFF for i in range(n))
    try:
        flag = flag_bytes.decode('utf-8')
    except UnicodeDecodeError:
        flag = ''.join(f'\\x{b:02x}' for b in flag_bytes)
    return flag


encoded_hex = "ccf2ef8e37445002c5a921313dbfd170be3111c58d59ff959efae104a44ddd83"

flag = decode(encoded_hex)
print("Recovered flag:")
print(flag)

