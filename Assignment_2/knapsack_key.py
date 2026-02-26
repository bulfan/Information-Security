import sys
import math


def is_superincreasing(sequence):
    total = 0
    for element in sequence:
        if element <= total:
            return False
        total += element
    return True


def is_private_key_valid(m, n, private_key):
    if not is_superincreasing(private_key):
        return False

    if n <= sum(private_key):
        return False

    if math.gcd(n, m) != 1:
        return False
    
    return True


def is_public_key_valid(m, n, private_key, public_key):
    if len(private_key) != len(public_key):
        return False
    for i in range(len(private_key)):
        expected = (m * private_key[i]) % n
        if expected != public_key[i]:
            return False
    
    return True


def parseinput(input_data):
    lines = input_data.strip().split('\n')

    m, n = map(int, lines[0].strip().split())

    private_key = list(map(int, lines[1].strip().split()))

    public_key = list(map(int, lines[2].strip().split()))
    
    return m, n, private_key, public_key


if __name__ == "__main__":
    input_data = sys.stdin.read()
    m, n, private_key, public_key = parseinput(input_data)
    
    if not is_private_key_valid(m, n, private_key):
        print(-1)

    elif not is_public_key_valid(m, n, private_key, public_key):
        print(0)
        
    else:
        print(1)