import sys


def mod_inverse(e, n):
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    
    _, x, _ = extended_gcd(e % n, n)
    return (x % n + n) % n


if __name__ == "__main__":
    all_input = sys.stdin.read().strip().split('\n')
    mode = all_input[0].strip()
    
    p, q, e = map(int, all_input[1].split())
    x = p * q
    n = (p - 1) * (q - 1)
    d = mod_inverse(e, n)

    values = list(map(int, all_input[2:]))
    
    if mode == 'e':
        result = [pow(value, e, x) for value in values]
    elif mode == 'd':
        result = [pow(value, d, x) for value in values]
    
    for val in result:
        print(val)
