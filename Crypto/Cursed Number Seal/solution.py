from Crypto.Util.number import long_to_bytes

c = long_to_bytes(5950244570109147723713809364954311287714173).decode()

f =5950244570109147723713809364954311287714173


print("c = ", c)





# Apply ROT15 cipher (because its decoded with rot11 so to decode it we apply 11mod26 = 15  to get the original text)


def rot15(text):


    result = []


    for ch in text:


        if 'a' <= ch <= 'z':


            result.append(chr((ord(ch) - ord('a') + 15) % 26 + ord('a')))


        elif 'A' <= ch <= 'Z':


            result.append(chr((ord(ch) - ord('A') + 15) % 26 + ord('A')))


        else:


            result.append(ch)


    return ''.join(result)





rot15_text = rot15(c)


print("the flag is : ", rot15_text)
