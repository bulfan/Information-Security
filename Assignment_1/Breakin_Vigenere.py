import sys
import math


def calculate_freq_vector(text, k):
    vec = [[0]*26 for _ in range(k)]
    pos = 0
    for char in text:
        if char.isalpha():
            subset = pos % k
            index = ord(char.lower()) - ord('a')
            vec[subset][index] += 1
            pos += 1
    return vec


def calculate_std(freq_vec):
    n = 26
    sumx = sum(freq_vec)
    if sumx == 0:
        return 0
    mean = sumx / n
    std = math.sqrt(sum(f ** 2 for f in freq_vec) / n - mean ** 2)
    return std


if __name__ == "__main__":
    lower_bound = int(input())
    upper_bound = int(input())
    text = sys.stdin.read()
    text = list(text.lower())
    max_std = 0
    result = [0, []]
    for k in range(lower_bound, upper_bound + 1):
        freq_vectors = calculate_freq_vector(text, k)
        std_sum = sum(calculate_std(vec) for vec in freq_vectors)
        if std_sum > max_std:
            max_std = std_sum
            result = [k, freq_vectors]
        print(f"The sum of {k} std. devs: {std_sum:.2f}")
    key = ''
    for vec in result[1]:
        index = vec.index(max(vec))
        shift = (index - 4) % 26  # ord(e) - ord('a') = 4
        key += chr(ord('a') + shift)
    
    print("\nKey guess:")
    print(key)
