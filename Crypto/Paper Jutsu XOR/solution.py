from itertools import zip_longest





# ===== challenge data =====


KEY1 = bytes.fromhex('a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313')


KEY2_XOR_KEY1 = bytes.fromhex('37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e')


KEY2_XOR_KEY3 = bytes.fromhex('c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1')


FLAG_XOR_ALL = bytes.fromhex('34dfd35e0cd505f291b0d05a3ac279957630812533e9b16d1fa7')





# ===== Step 1: Derive keys =====


# KEY2 = KEY2 ^ KEY1


KEY2 = bytes(a ^ b for a, b in zip_longest(KEY2_XOR_KEY1, KEY1, fillvalue=0))





# KEY3 = KEY2 ^ (KEY2 ^ KEY3)


KEY3 = bytes(a ^ b for a, b in zip_longest(KEY2_XOR_KEY3, KEY2, fillvalue=0))





# ===== Step 2: Recover the flag =====


# Use zip_longest to prevent truncation


FLAG = bytes(a ^ b ^ c ^ d for a, b, c, d in zip_longest(FLAG_XOR_ALL, KEY1, KEY2, KEY3, fillvalue=0))





# ===== Step 3: Print =====

print("Flag:", FLAG.decode())

