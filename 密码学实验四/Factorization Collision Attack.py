# 因数碰撞攻击

import gmpy2
import binascii

n = []
e = []
c = []
name = ['Frame1','Frame18']

for i in name:
    f = open(i,'r')
    data = f.read()
    n0 , e0 , c0 = int(data[:256] , 16) , int(data[256:512] , 16) , int(data[512:] , 16)
    n.append(n0)
    e.append(e0)
    c.append(c0)

prime = gmpy2.gcd(n[0],n[1])

if prime != 1:
    p_of_frame = prime

q_of_frame1 = n[0] // p_of_frame
q_of_frame18 = n[1] // p_of_frame

phi_of_frame1 = (p_of_frame-1)*(q_of_frame1-1)
phi_of_frame18 = (p_of_frame-1)*(q_of_frame18-1)

d_of_frame1 = gmpy2.invert(e[0] ,phi_of_frame1)
d_of_frame18 = gmpy2.invert(e[1], phi_of_frame18)

plaintext_of_frame1 = gmpy2.powmod(c[0], d_of_frame1, n[0])
plaintext_of_frame18 = gmpy2.powmod(c[1], d_of_frame18,n[1])

final_plain_of_frame1 = binascii.a2b_hex(hex(plaintext_of_frame1)[2:])
final_plain_of_frame18 = binascii.a2b_hex(hex(plaintext_of_frame18)[2:])

print(final_plain_of_frame1[-8:])
print(final_plain_of_frame18[-8:])