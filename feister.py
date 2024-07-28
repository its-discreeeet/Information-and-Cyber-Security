#pt = 0100111101001011
#k1 = 10100110
#k2 = 10110111


def get_16bit_binary_input():
    while True:
        plain_text = input("Enter a 16-bit binary number: ")
        if len(plain_text) == 16 and all(char in '01' for char in plain_text):
            return plain_text
        else:
            print("Invalid input. Please enter exactly 16 bits (0s and 1s only).")

def get_8bit_key():
    while True:
        key = input("Enter an 8-bit binary key: ")
        if len(key) == 8 and all(char in '01' for char in key):
            return key
        else:
            print("Invalid input. Please enter exactly 8 bits (0s and 1s only).")

def XOR(a, b):
    return ''.join(str(int(x) ^ int(y)) for x, y in zip(a, b))

def split(plain_text):
    left = plain_text[:8]
    right = plain_text[8:]
    return left, right

def feistel_round(left, right, key):
    new_right = XOR(right, key)
    new_left = XOR(left, new_right)
    return new_left, right

# Encryption
plain_text = get_16bit_binary_input()
print("Entered plain_text is:", plain_text)

k1 = get_8bit_key()
k2 = get_8bit_key()
print("Entered key1 is:", k1)
print("Entered key2 is:", k2)

left, right = split(plain_text)
print("Initial split - Left:", left, "Right:", right)

left, right = feistel_round(left, right, k1)
left, right = right, left
print("After round 1 - Left:", left, "Right:", right)

left, right = feistel_round(left, right, k2)
left, right = right, left
print("After round 2 - Left:", left, "Right:", right)

cipher_text = right + left
print("Cipher text is:", cipher_text)

# Decryption
def decrypt_feistel(cipher_text, k1, k2):
    left, right = split(cipher_text)
    print("Initial split - Left:", left, "Right:", right)
    
    left, right = right, left
    left, right = feistel_round(left, right, k2)
    print("After round 1 - Left:", left, "Right:", right)
    
    left, right = right, left
    left, right = feistel_round(left, right, k1)
    print("After round 2 - Left:", left, "Right:", right)
    
    plain_text = right + left
    return plain_text

decrypted_text = decrypt_feistel(cipher_text, k1, k2)
print("Decrypted text is:", decrypted_text)

