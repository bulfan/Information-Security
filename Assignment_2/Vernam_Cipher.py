import sys


if __name__ == "__main__":
    all_input = sys.stdin.buffer.read()
    total_len = len(all_input)
    len_data = (total_len - 1) // 2
    if all_input[len_data] == 0xFF:
        key = all_input[:len_data]
        data = all_input[len_data + 1:]
        result = bytearray(len_data)
        for i in range(len_data):
            result[i] = key[i] ^ data[i]
        sys.stdout.buffer.write(result)
        sys.stdout.buffer.flush()
