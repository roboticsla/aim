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

def decrypt_block(cipher_text, key):
    round_key = key_expansion(key)
    state = add_round_key(cipher_text, round_key)
    state = inverse_mix_columns(state)
    state = inverse_shift_row(state)
    state = bytes(inverse_s_box(b) for b in state)
    state = add_round_key(state, key)
    return state
    
def receive_from_client(data, key):
    received_array = bytes(map(int, data.split()))
    decrypted = decrypt_block(received_array, key)
    return decrypted


if __name__ == "__main__":
    host = '127.0.0.1'
    port = 65432
    key = b'\x89\xAB\xCD\xEF' 
    
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(2)
    print("Server listening on port", port)

    conn, address = server_socket.accept()
    print(f"Connection from {address} has been established.")

    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        print(f"Received encrypted message: {data}")
        
        decrypted_message = receive_from_client(data, key)
        print(f"Decrypted message: {decrypted_message}")

    conn.close()
