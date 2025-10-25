cipher = bytes.fromhex("0919682118080f0e6905026a08056e0e0e6e191127")


print (cipher)

# (you need to brute for the key)
key = 0x5A


plain = bytes([b ^ key for b in cipher])


print(plain.decode())  # -> SC2{BRUT3_X0R_4TT4CK}
