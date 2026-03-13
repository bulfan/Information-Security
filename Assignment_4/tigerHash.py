import sys
import struct

MASK64 = 0xFFFFFFFFFFFFFFFF

# Note: For a fully functional cryptographic hash, these S-Boxes MUST be 
# populated with the standard 1024 Tiger 64-bit constants. 
# They are mocked here as zero-arrays to allow the structure to run.
S0 = [0] * 256
S1 = [0] * 256
S2 = [0] * 256
S3 = [0] * 256

def inner_round(a, b, c, x, mul):
    c = (c ^ x) & MASK64
    
    # Extract bytes from 'c' for the S-Box lookups (little-endian byte order)
    a = (a - (S0[c & 0xFF] ^ 
              S1[(c >> 16) & 0xFF] ^ 
              S2[(c >> 32) & 0xFF] ^ 
              S3[(c >> 48) & 0xFF])) & MASK64
              
    b = (b + (S3[(c >> 8) & 0xFF] ^ 
              S2[(c >> 24) & 0xFF] ^ 
              S1[(c >> 40) & 0xFF] ^ 
              S0[(c >> 56) & 0xFF])) & MASK64
              
    b = (b * mul) & MASK64
    return a, b, c

def key_schedule(w):
    # Pass 1 of Key Schedule (incorporating Figure 5.1 corrections)
    w[0] = (w[0] - (w[7] ^ 0xA5A5A5A5A5A5A5A5)) & MASK64
    w[1] = (w[1] ^ w[0]) & MASK64
    w[2] = (w[2] + w[1]) & MASK64
    w[3] = (w[3] - (w[2] ^ (~w[1] & MASK64))) & MASK64
    w[4] = (w[4] ^ w[3]) & MASK64
    w[5] = (w[5] + w[4]) & MASK64
    w[6] = (w[6] - (w[5] ^ (~w[4] & MASK64))) & MASK64
    w[7] = (w[7] ^ w[6]) & MASK64
    
    # Pass 2 of Key Schedule
    w[0] = (w[0] + w[7]) & MASK64
    w[1] = (w[1] - (w[0] ^ (~w[7] & MASK64))) & MASK64
    w[2] = (w[2] ^ w[1]) & MASK64
    w[3] = (w[3] + w[2]) & MASK64
    w[4] = (w[4] - (w[3] ^ (~w[2] & MASK64))) & MASK64
    w[5] = (w[5] ^ w[4]) & MASK64
    w[6] = (w[6] + w[5]) & MASK64
    w[7] = (w[7] - (w[6] ^ (~w[5] & MASK64))) & MASK64
    return w

if __name__ == "__main__":
    all_input = sys.stdin.buffer.read()
    orig_len_bytes = len(all_input)
    padded_message = bytearray(all_input)
    padded_message.append(0x01)
    while len(padded_message) % 64 != 56:
        padded_message.append(0x00)
    padded_message += struct.pack('<Q', orig_len_bytes * 8)
    
    # 2. Initialize State Registers
    a = 0x0123456789ABCDEF
    b = 0xFEDCBA9876543210
    c = 0xF096A5B4C3B2E187
    
    # 3. Process each 512-bit (64-byte) block
    for i in range(0, len(padded_message), 64):
        block = padded_message[i:i+64]
        
        # Unpack 64 bytes into 8 64-bit unsigned integers (little-endian)
        w = list(struct.unpack('<8Q', block))
        
        # Save old values for the feedforward step later
        aa, bb, cc = a, b, c
        
        # F_5 (Outer Round 1)
        a, b, c = inner_round(a, b, c, w[0], 5)
        b, c, a = inner_round(b, c, a, w[1], 5)
        c, a, b = inner_round(c, a, b, w[2], 5)
        a, b, c = inner_round(a, b, c, w[3], 5)
        b, c, a = inner_round(b, c, a, w[4], 5)
        c, a, b = inner_round(c, a, b, w[5], 5)
        a, b, c = inner_round(a, b, c, w[6], 5)
        b, c, a = inner_round(b, c, a, w[7], 5)
        
        w = key_schedule(w)
        
        # F_7 (Outer Round 2)
        c, a, b = inner_round(c, a, b, w[0], 7)
        a, b, c = inner_round(a, b, c, w[1], 7)
        b, c, a = inner_round(b, c, a, w[2], 7)
        c, a, b = inner_round(c, a, b, w[3], 7)
        a, b, c = inner_round(a, b, c, w[4], 7)
        b, c, a = inner_round(b, c, a, w[5], 7)
        c, a, b = inner_round(c, a, b, w[6], 7)
        a, b, c = inner_round(a, b, c, w[7], 7)
        
        w = key_schedule(w)
        
        # F_9 (Outer Round 3)
        b, c, a = inner_round(b, c, a, w[0], 9)
        c, a, b = inner_round(c, a, b, w[1], 9)
        a, b, c = inner_round(a, b, c, w[2], 9)
        b, c, a = inner_round(b, c, a, w[3], 9)
        c, a, b = inner_round(c, a, b, w[4], 9)
        a, b, c = inner_round(a, b, c, w[5], 9)
        b, c, a = inner_round(b, c, a, w[6], 9)
        c, a, b = inner_round(c, a, b, w[7], 9)
        
        # 4. Feedforward Layer (as seen in Figure 5.2 bottom)
        a = (a ^ aa) & MASK64
        b = (b - bb) & MASK64
        c = (c + cc) & MASK64
        
    # Final step: output the concatenated 192-bit hash value to stdout
    result = struct.pack('<3Q', a, b, c)
    sys.stdout.buffer.write(result)
    sys.stdout.buffer.flush()