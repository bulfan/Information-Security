import sys


if __name__ == "__main__":
    requests = input().split()
    text = sys.stdin.read()
    text = list(text)
    transformations = "abcdefghijklmnopqrstuvwxyz"
    transformations = list(transformations)
    for i in range(0, len(requests), 2):
        request = requests[i]
        key = requests[i + 1]
        if (not key.isalpha() and int(key) % 26 == 0) or key == "abcdefghijklmnopqrstuvwxyz":
            continue
        if not key.isalpha():
            key = int(key) % 26
            if request == "e":
                for j in range(26):
                    transformations[j] = chr((ord(transformations[j]) - ord('a') + key) % 26 + ord('a'))
            elif request == "d":
                for j in range(26):
                    transformations[j] = chr((ord(transformations[j]) - ord('a') - key) % 26 + ord('a'))
        else:
            key = list(key)
            if request == "e":
                for j in range(26):
                    transformations[j] = key[ord(transformations[j]) - ord('a')]
            elif request == "d":
                key = list(key)
                for j in range(26):
                    transformations[j] = chr(key.index(transformations[j]) + ord('a'))
    for i in range(len(text)):
        if text[i].isalpha():
            if text[i].isupper():
                text[i] = transformations[ord(text[i]) - ord('A')].upper()
            else:
                text[i] = transformations[ord(text[i]) - ord('a')]
    print(''.join(text), end="")