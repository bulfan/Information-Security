import sys
from SBoxes import S0, S1, S2, S3

mask = 0xFFFFFFFFFFFFFFFF


def inner_round(a, b, c, x, mul):
    c = (c ^ x) & mask
    a = (a - (S0[c & 0xFF] ^
              S1[(c >> 16) & 0xFF] ^
              S2[(c >> 32) & 0xFF] ^
              S3[(c >> 48) & 0xFF])) & mask
    b = (b + (S3[(c >> 8) & 0xFF] ^
              S2[(c >> 24) & 0xFF] ^
              S1[(c >> 40) & 0xFF] ^
              S0[(c >> 56) & 0xFF])) & mask
    b = (b * mul) & mask
    return a, b, c


def key_schedule(w):
    w[0] = (w[0] - (w[7] ^ 0xA5A5A5A5A5A5A5A5)) & mask
    w[1] = (w[1] ^ w[0]) & mask
    w[2] = (w[2] + w[1]) & mask
    w[3] = (w[3] - (w[2] ^ (((~w[1] & mask) << 19)& mask))) & mask
    w[4] = (w[4] ^ w[3]) & mask
    w[5] = (w[5] + w[4]) & mask
    w[6] = (w[6] - (w[5] ^ (((~w[4] & mask) >> 23) & mask))) & mask
    w[7] = (w[7] ^ w[6]) & mask

    w[0] = (w[0] + w[7]) & mask
    w[1] = (w[1] - (w[0] ^ (((~w[7] & mask) << 19) & mask))) & mask
    w[2] = (w[2] ^ w[1]) & mask
    w[3] = (w[3] + w[2]) & mask
    w[4] = (w[4] - (w[3] ^ (((~w[2] & mask) >> 23) & mask))) & mask
    w[5] = (w[5] ^ w[4]) & mask
    w[6] = (w[6] + w[5]) & mask
    w[7] = (w[7] - (w[6] ^ 0x0123456789abcdef)) & mask
    return w


if __name__ == "__main__":
    all_input = sys.stdin.buffer.read()
    padded_msg = bytearray(all_input)
    padded_msg.append(0x01)
    while len(padded_msg) % 64 != 56:
        padded_msg.append(0x00)
    original_len = len(all_input) * 8
    padded_msg += original_len.to_bytes(8, byteorder='little')

    a = 0x0123456789ABCDEF
    b = 0xFEDCBA9876543210
    c = 0xF096A5B4C3B2E187
    for i in range(0, len(padded_msg), 64):
        block = padded_msg[i:i+64]
        aa, bb, cc = a, b, c

        w = [int.from_bytes(block[j:j+8], byteorder='little') for j in range(0, 64, 8)]
        a, b, c = inner_round(a, b, c, w[0], 5)
        b, c, a = inner_round(b, c, a, w[1], 5)
        c, a, b = inner_round(c, a, b, w[2], 5)
        a, b, c = inner_round(a, b, c, w[3], 5)
        b, c, a = inner_round(b, c, a, w[4], 5)
        c, a, b = inner_round(c, a, b, w[5], 5)
        a, b, c = inner_round(a, b, c, w[6], 5)
        b, c, a = inner_round(b, c, a, w[7], 5)

        w = key_schedule(w)
        c, a, b = inner_round(c, a, b, w[0], 7)
        a, b, c = inner_round(a, b, c, w[1], 7)
        b, c, a = inner_round(b, c, a, w[2], 7)
        c, a, b = inner_round(c, a, b, w[3], 7)
        a, b, c = inner_round(a, b, c, w[4], 7)
        b, c, a = inner_round(b, c, a, w[5], 7)
        c, a, b = inner_round(c, a, b, w[6], 7)
        a, b, c = inner_round(a, b, c, w[7], 7)

        w = key_schedule(w)
        b, c, a = inner_round(b, c, a, w[0], 9)
        c, a, b = inner_round(c, a, b, w[1], 9)
        a, b, c = inner_round(a, b, c, w[2], 9)
        b, c, a = inner_round(b, c, a, w[3], 9)
        c, a, b = inner_round(c, a, b, w[4], 9)
        a, b, c = inner_round(a, b, c, w[5], 9)
        b, c, a = inner_round(b, c, a, w[6], 9)
        c, a, b = inner_round(c, a, b, w[7], 9)

        a = (a ^ aa) & mask
        b = (b - bb) & mask
        c = (c + cc) & mask

    result = (a.to_bytes(8, byteorder='little') +
              b.to_bytes(8, byteorder='little') +
              c.to_bytes(8, byteorder='little'))
    sys.stdout.buffer.write(result)
    sys.stdout.buffer.flush()
