import sys


def encrypt(block, key):
    lh = block[:4]
    rh = block[4:]
    new_lh = rh
    rh = bytes(lh[i] ^ F(rh, key)[i] for i in range(4))
    lh = new_lh
    return rh + lh


def decrypt(block, key):
    lh = block[:4]
    rh = block[4:]
    new_rh = lh
    lh = bytes(rh[i] ^ F(lh, key)[i] for i in range(4))
    rh = new_rh
    return rh + lh


def F(rh, key):
    return bytes(rh[i] ^ key[i % len(key)] for i in range(len(rh)))


if __name__ == "__main__":
    all_input = sys.stdin.buffer.read()

    separator = all_input.index(0xFF)
    mode = all_input[:separator]
    all_input = all_input[separator + 1:]

    separator = all_input.index(0xFF)
    key = all_input[:separator]
    data = all_input[separator + 1:]

    result = bytearray()
    for i in range(0, len(data), 8):
        block = data[i:i + 8]
        if mode == b'd':
            result.extend(decrypt(block, key))
        else:
            result.extend(encrypt(block, key))

    result = bytes(result)
    sys.stdout.buffer.write(result)
    sys.stdout.buffer.flush()