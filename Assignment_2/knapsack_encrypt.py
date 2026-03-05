import sys


def mod_inverse(m, n):
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    
    _, x, _ = extended_gcd(m % n, n)
    return (x % n + n) % n


def encrypt(public_key, plaintext_values):
    ciphertext = []
    key_length = len(public_key)
    
    for value in plaintext_values:
        cipher_sum = 0
        for i in range(key_length):
            if (value >> i) & 1:
                cipher_sum += public_key[i]
        ciphertext.append(cipher_sum)
    
    return ciphertext


def decrypt(m, n, private_key, ciphertext_values):
    m_inverse = mod_inverse(m, n)
    plaintext = []
    key_length = len(private_key)
    
    for cipher_value in ciphertext_values:
        s = (cipher_value * m_inverse) % n

        plain_value = 0
        for i in range(key_length - 1, -1, -1):
            if private_key[i] <= s:
                s -= private_key[i]
                plain_value |= (1 << i)
        
        plaintext.append(plain_value)
    
    return plaintext


def parse_input(input_data):
    lines = input_data.strip().split('\n')
    mode = lines[0].strip()

    if mode == 'e':
        public_key = list(map(int, lines[1].strip().split()))
        values = [int(lines[i].strip()) for i in range(2, len(lines))]
        return mode, public_key, None, None, values
    
    elif mode == 'd':
        m, n = map(int, lines[1].strip().split())
        private_key = list(map(int, lines[2].strip().split()))
        values = [int(lines[i].strip()) for i in range(3, len(lines))]
        return mode, None, m, n, private_key, values


if __name__ == "__main__":
    input_data = sys.stdin.read()
    parsed = parse_input(input_data)
    mode = parsed[0]
    
    if mode == 'e':
        _, public_key, _, _, values = parsed
        result = encrypt(public_key, values)
    
    elif mode == 'd':
        _, _, m, n, private_key, values = parsed
        result = decrypt(m, n, private_key, values)

    for val in result:
        print(val)
