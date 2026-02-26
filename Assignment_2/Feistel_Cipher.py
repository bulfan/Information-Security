import sys


def feistel(lh, rh, round_key):
    new_lh = rh
    new_rh = bytes(lh[i] ^ round_key[i] for i in range(4))
    return new_lh, new_rh


def encrypt(block, keys):
    lh = block[:4]
    rh = block[4:]
    for round_key in keys:
        lh, rh = feistel(lh, rh, round_key)
    return lh + rh


def decrypt(block, keys):
    lh = block[:4]
    rh = block[4:]
    for round_key in keys:
        lh, rh = feistel(lh, rh, round_key)
    return lh + rh


if __name__ == "__main__":
    all_input = sys.stdin.buffer.read()

    separator = all_input.index(0xFF)
    mode = all_input[:separator]
    all_input = all_input[separator + 1:]

    separator = all_input.index(0xFF)
    key_bytes = all_input[:separator]
    data = all_input[separator + 1:]

    keys = [key_bytes[i:i + 4] for i in range(0, len(key_bytes), 4)]

    result = bytearray()
    for i in range(0, len(data), 8):
        block = data[i:i + 8]
        if mode == bytes([0x64]):
            result.extend(decrypt(block, keys))
        else:
            result.extend(encrypt(block, keys))

    sys.stdout.buffer.write(bytes(result))
    sys.stdout.buffer.flush()