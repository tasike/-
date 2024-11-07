# from math import gcd

# p = 1009
# q = 3643
# n = p * q
# phi = (p - 1) * (q - 1)

# sum = 0
# min_nonencryption = n    # 最小未加密信息的数目
# for e in range(2, phi):
#     if gcd(e, phi) == 1:
#         nonencryption = 0  # 未加密信息的数目
#         for m in range(n):
#             if pow(m, e, n) == m:
#                 nonencryption += 1
#         if nonencryption < min_nonencryption:
#             min_nonencryption = nonencryption
#             sum = e
#         elif nonencryption == min_nonencryption:
#             sum += e
# print(sum)


from math import gcd

p = 1009
q = 3643
n = p * q
phi = (p - 1) * (q - 1)

sum = 0
for e in range(3, phi, 2):
    if gcd(e, phi) == 1 and gcd(e - 1, p - 1) == 2 and gcd(e - 1, q - 1) == 2:
        sum += e
print(sum)