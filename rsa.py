
'''
LOGIC

Key generation :
select p,q
calculate n = p X q
calculate totient(n) = (p-1)(q-1)
select e = gcd(e,totion(n)) = 1 where 1<e<totient(n)
calculate d ≡ e^(-1) mod totient(n)
public key = [n,e]
private key = [n,d]


Encryption :
select plaintext
select ciphertext = plaintext^e mod n

Decryption :
select plaintext = ciphertext^d mod n

'''

import random
from sympy import isprime

def generate_prime(range_start, range_end):
    while True:
        num = random.randint(range_start, range_end)
        if isprime(num):
            return num

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def generate_keys():

    p = generate_prime(100, 300)
    q = generate_prime(100, 300)
    
    n = p * q

    totient = (p - 1) * (q - 1)
    
    # Here we select e such that 1 < e < totient and gcd(e, totient) = 1
    while True:
        e = random.randint(2, totient - 1)
        if gcd(e, totient) == 1:
            break
    
   #calculating d
    k = 1
    while k<e:
        d = (1 + k * totient) / e
        if d.is_integer():
            d = int(d)
            break
        k += 1
    
    # Public key (n, e) and private key (n, d)
    return (n, e), (n, d)


def encrypt(plain_text, public_key):
    n, e = public_key
    cipher_text = [pow(ord(char), e, n) for char in plain_text]
    return cipher_text


def decrypt(cipher_text, private_key):
    n, d = private_key
    plain_text = ''.join([chr(pow(char, d, n)) for char in cipher_text])
    return plain_text

def main():
    public_key, private_key = generate_keys()
    
    print("Public Key: ", public_key)
    print("Private Key: ", private_key)
    
    plain_text = input("Enter the plaintext: ")
    encrypted_msg = encrypt(plain_text, public_key)
    print("Encrypted message: ", encrypted_msg)
    
    decrypted_msg = decrypt(encrypted_msg, private_key)
    print("Decrypted message: ", decrypted_msg)

if __name__ == "__main__":
    main()
