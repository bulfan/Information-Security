import sys


def encrypt(text, key):
    result = []
    key_index = 0
    for char in text:
        if char.isalpha():
            shift = ord(key[key_index % len(key)].lower()) - ord('a')
            if char.isupper():
                result.append(chr((ord(char) - ord('A') + shift) % 26 + ord('A')))
            else:
                result.append(chr((ord(char) - ord('a') + shift) % 26 + ord('a')))
            key_index += 1
        else:
            result.append(char)
    return result


def decrypt(text, key):
    result = []
    key_index = 0
    for char in text:
        if char.isalpha():
            shift = ord(key[key_index % len(key)].lower()) - ord('a')
            if char.isupper():
                result.append(chr((ord(char) - ord('A') - shift) % 26 + ord('A')))
            else:
                result.append(chr((ord(char) - ord('a') - shift) % 26 + ord('a')))
            key_index += 1
        else:
            result.append(char)
    return result


if __name__ == "__main__":
    requests = input().split()
    key = requests[1]
    text = sys.stdin.read()
    text = list(text)
    
    if requests[0] == "e":
        text = encrypt(text, key)
    elif requests[0] == "d":
        text = decrypt(text, key)
    
    print(''.join(text), end="")