import sys


if __name__ == "__main__":
    all_input = sys.stdin.buffer.read()
    separator = all_input.index(0xFF)
    key = all_input[:separator]
    data = all_input[separator + 1:]
    len_data = len(data)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    i = 0
    j = 0
    for t in range(256):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
    result = bytearray(len_data)
    for k in range(len_data):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        result[k] = data[k] ^ S[(S[i] + S[j]) % 256]
    sys.stdout.buffer.write(result)
    sys.stdout.buffer.flush()