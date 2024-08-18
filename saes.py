import sys


SBOX = [
    0x9, 0x4, 0xA, 0xB,
    0xD, 0x1, 0x8, 0x5,
    0x6, 0x2, 0x0, 0x3,
    0xC, 0xE, 0xF, 0x7
]


INV_SBOX = [
    0xA, 0x5, 0x9, 0xB,
    0x1, 0x7, 0x8, 0xF,
    0x6, 0x0, 0x2, 0x3,
    0xC, 0x4, 0xD, 0xE
]


MIX_COLS_MATRIX = [
    [1, 4],
    [4, 1]
]

INV_MIX_COLS_MATRIX = [
    [9, 2],
    [2, 9]
]

def debug_print(step, state):
    print(f"{step}: {state:04X}")

def is_hexadecimal(ch):
    return ch in '0123456789ABCDEFabcdef'

def nibble_substitution(input_nibble, sbox):
    output_nibble = 0
    for i in range(4):
        nibble = (input_nibble >> (4 * i)) & 0xF
        output_nibble |= (sbox[nibble] << (4 * i))
    return output_nibble

def shift_rows(nibble):
    return ((nibble & 0xF0F0) | ((nibble & 0x0F00) >> 8) | ((nibble & 0x000F) << 8))

def mix_columns(nibble):
    a = (nibble >> 12) & 0xF
    b = (nibble >> 8) & 0xF
    c = (nibble >> 4) & 0xF
    d = nibble & 0xF
    
    new_a = multiply(1, a) ^ multiply(4, b)
    new_b = multiply(4, a) ^ multiply(1, b)
    new_c = multiply(1, c) ^ multiply(4, d)
    new_d = multiply(4, c) ^ multiply(1, d)
    
    return (new_a << 12) | (new_b << 8) | (new_c << 4) | new_d

def inv_mix_columns(nibble):
    a = (nibble >> 12) & 0xF
    b = (nibble >> 8) & 0xF
    c = (nibble >> 4) & 0xF
    d = nibble & 0xF
    
    new_a = multiply(9, a) ^ multiply(2, b)
    new_b = multiply(2, a) ^ multiply(9, b)
    new_c = multiply(9, c) ^ multiply(2, d)
    new_d = multiply(2, c) ^ multiply(9, d)
    
    return (new_a << 12) | (new_b << 8) | (new_c << 4) | new_d

def multiply(a, b):
    result = 0
    while b:
        if b & 1:
            result ^= a
        a <<= 1
        if a & 0x10:
            a ^= 0x13
        b >>= 1
    return result & 0xF

def add_round_key(state, key):
    return (state ^ key) & 0xFFFF

def key_expansion(key):
    w = [0] * 6
    w[0] = (key >> 8) & 0xFF
    w[1] = key & 0xFF
    w[2] = (w[0] ^ 0x80 ^ nibble_substitution(w[1], SBOX)) & 0xFF
    w[3] = (w[2] ^ w[1]) & 0xFF
    w[4] = (w[2] ^ 0x30 ^ nibble_substitution(w[3], SBOX)) & 0xFF
    w[5] = (w[4] ^ w[3]) & 0xFF
    return (w[0] << 8) | w[1], (w[2] << 8) | w[3], (w[4] << 8) | w[5]

def saes_encrypt(plain_text, key):
    round_keys = key_expansion(key)
    debug_print("Initial state", plain_text)
    state = add_round_key(plain_text, round_keys[0])
    debug_print("After initial add round key", state)
    
    # Round 1
    state = nibble_substitution(state, SBOX) & 0xFFFF
    debug_print("After nibble substitution", state)
    state = shift_rows(state) & 0xFFFF
    debug_print("After shift rows", state)
    state = mix_columns(state) & 0xFFFF
    debug_print("After mix columns", state)
    state = add_round_key(state, round_keys[1])
    debug_print("After round 1 add round key", state)
    
    # Round 2
    state = nibble_substitution(state, SBOX) & 0xFFFF
    debug_print("After final nibble substitution", state)
    state = shift_rows(state) & 0xFFFF
    debug_print("After final shift rows", state)
    cipher_text = add_round_key(state, round_keys[2])
    debug_print("Final cipher text", cipher_text)
    return cipher_text

def saes_decrypt(cipher_text, key):
    round_keys = key_expansion(key)
    debug_print("Initial state", cipher_text)
    state = add_round_key(cipher_text, round_keys[2])
    debug_print("After initial add round key", state)
    
    # Round 1
    state = shift_rows(state) & 0xFFFF
    debug_print("After shift rows", state)
    state = nibble_substitution(state, INV_SBOX) & 0xFFFF
    debug_print("After nibble substitution", state)
    state = add_round_key(state, round_keys[1])
    debug_print("After add round key", state)
    state = inv_mix_columns(state) & 0xFFFF
    debug_print("After inv mix columns", state)
    
    # Round 2
    state = shift_rows(state) & 0xFFFF
    debug_print("After shift rows", state)
    state = nibble_substitution(state, INV_SBOX) & 0xFFFF
    debug_print("After final nibble substitution", state)
    plain_text = add_round_key(state, round_keys[0])
    debug_print("Final plain text", plain_text)
    return plain_text

def print_key_expansion(key):
    round_keys = key_expansion(key)
    print(f"Key: {key:04X}")
    print(f"Round Key 0: {round_keys[0]:04X}")
    print(f"Round Key 1: {round_keys[1]:04X}")
    print(f"Round Key 2: {round_keys[2]:04X}")

def main():
    if len(sys.argv) != 4:
        print("ERROR: Invalid number of parameters\nExpects: <ENC|DEC> <key> <data>")
        return

    operation = sys.argv[1]

    if operation not in ["ENC", "DEC"]:
        print("ERROR: Invalid Operation")
        return

    key_string = sys.argv[2]

    if len(key_string) != 4 or not all(is_hexadecimal(ch) for ch in key_string):
        print("ERROR: Invalid Key length or non-hex characters in key")
        return

    key = int(key_string, 16)

    print_key_expansion(key)

    if operation == "ENC":
        plain_text_string = sys.argv[3]
        if len(plain_text_string) != 4 or not all(is_hexadecimal(ch) for ch in plain_text_string):
            print("ERROR: Invalid Data length or non-hex characters in data")
            return

        plain_text = int(plain_text_string, 16)
        cipher_text = saes_encrypt(plain_text, key)
        print(f"Cipher text is: {cipher_text:04X}")

    elif operation == "DEC":
        cipher_text_string = sys.argv[3]
        if len(cipher_text_string) != 4 or not all(is_hexadecimal(ch) for ch in cipher_text_string):
            print("ERROR: Invalid Data length or non-hex characters in data")
            return

        cipher_text = int(cipher_text_string, 16)
        plain_text = saes_decrypt(cipher_text, key)
        print(f"Plain text is: {plain_text:04X}")

if __name__ == "__main__":
    main()