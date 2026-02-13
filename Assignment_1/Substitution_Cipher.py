import sys


def encrypt(text, key):
    if (not key.isalpha() and int(key) % 26 == 0) or key == "abcdefghijklmnopqrstuvwxyz":
        return text
    if not key.isalpha():
        key = int(key) % 26
        for i in range(len(text)):
            if text[i].isalpha():
                if text[i].isupper():
                    text[i] = chr((ord(text[i]) - ord('A') + key) % 26 + ord('A'))
                else:
                    text[i] = chr((ord(text[i]) - ord('a') + key) % 26 + ord('a'))
    else:
        key = list(key)
        for i in range(len(text)):
            if text[i].isalpha():
                if text[i].isupper():
                    text[i] = key[ord(text[i]) - ord('A')].upper()
                else:
                    text[i] = key[ord(text[i]) - ord('a')].lower()
    return text


def decrypt(text, key):
    if (not key.isalpha() and int(key) % 26 == 0) or key == "abcdefghijklmnopqrstuvwxyz":
        return text
    if not key.isalpha():
        key = int(key) % 26
        for i in range(len(text)):
            if text[i].isalpha():
                if text[i].isupper():
                    text[i] = chr((ord(text[i]) - ord('A') - key) % 26 + ord('A'))
                else:
                    text[i] = chr((ord(text[i]) - ord('a') - key) % 26 + ord('a'))
    else:
        key = list(key)
        for i in range(len(text)):
            if text[i].isalpha():
                if text[i].isupper():
                    text[i] = chr(key.index(text[i].lower()) + ord('A'))
                else:
                    text[i] = chr(key.index(text[i]) + ord('a'))
    return text


if __name__ == "__main__":
    requests = input().split()
    text = sys.stdin.read()
    text = list(text)
    for i in range(0, len(requests), 2):
        request = requests[i]
        key = requests[i + 1]
        if request == "e":
            text = encrypt(text, key)
        elif request == "d":
            text = decrypt(text, key)
    print(''.join(text), end="")