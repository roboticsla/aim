import socket

def xor_bytes(a, b):
    return bytes(i ^ j for i, j in zip(a, b))

def rotate_left(byte, n):
    return ((byte << n) & 0xFF) | (byte >> (8 - n))

def rotate_right(byte, n):
    return ((byte >> n) | (byte << (8 - n))) & 0xFF

def s_box(byte):
    sbox = [0x6, 0x4, 0xC, 0x5, 0x0, 0x7, 0x2, 0xE, 
            0x1, 0xF, 0x3, 0xD, 0xA, 0x9, 0xB, 0x8]
    return sbox[byte & 0x0F]

def inverse_s_box(byte):
    inv_sbox = [0x4, 0x8, 0x6, 0xA, 0x1, 0x3, 0x0, 0x5, 
                0xE, 0xD, 0xC, 0xF, 0x2, 0xB, 0x7, 0x9]
    return inv_sbox[byte & 0x0F]

def shift_row(state):
    return [state[0], state[1], rotate_left(state[2], 1), rotate_left(state[3], 1)]

def inverse_shift_row(state):
    return [state[0], state[1], rotate_right(state[2], 1), rotate_right(state[3], 1)]

def mix_columns(state):
    return [state[0] ^ state[1], state[1] ^ state[2], state[2] ^ state[3], state[3] ^ state[0]]

def inverse_mix_columns(state):
    return mix_columns(state) 

def add_round_key(state, round_key):
    return xor_bytes(state, round_key)

def key_expansion(key):
    return [rotate_left(k, 1) for k in key]

# Simplified AES functions

def encrypt_block(plain_text, key):
    state = add_round_key(plain_text, key)
    state = bytes(s_box(b) for b in state)
    state = shift_row(state)
    state = mix_columns(state)
    round_key = key_expansion(key)
    state = add_round_key(state, round_key)
    return state

def send_to_server(cipher_text):
    host = '127.0.0.1'
    port = 65432
    client_socket = socket.socket()
    client_socket.connect((host, port))
    print("\nSending encrypted data to server...")
    
    data = ' '.join(str(b) for b in cipher_text)
    client_socket.send(data.encode())
    client_socket.close()

if __name__ == "__main__":
    plain_text = b'\x01\x23\x45\x67'  # 4 bytes of plain text
    key = b'\x89\xAB\xCD\xEF'         # 4 bytes of key

    cipher_text = encrypt_block(plain_text, key)
    print("Encrypted:", cipher_text)
    send_to_server(cipher_text)

