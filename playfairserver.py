import socket

def generate_playfair_table(key):
    # Remove duplicates while maintaining order
    key = ''.join(sorted(set(key), key=key.index))
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    table = []
    for char in key:
        if char not in table:
            table.append(char)
    for char in alphabet:
        if char not in table:
            table.append(char)
    return [table[i:i+5] for i in range(0, 25, 5)]

def find_position(char, table):
    for row in range(5):
        for col in range(5):
            if table[row][col] == char:
                return row, col
    return None

def playfair_decrypt(text, key):
    table = generate_playfair_table(key)
    decrypted_text = ""
    
    i = 0
    while i < len(text):
        a = text[i]
        b = text[i + 1]
        i += 2
        
        row_a, col_a = find_position(a, table)
        row_b, col_b = find_position(b, table)
        
        if row_a == row_b:
            decrypted_text += table[row_a][(col_a - 1) % 5]
            decrypted_text += table[row_b][(col_b - 1) % 5]
        elif col_a == col_b:
            decrypted_text += table[(row_a - 1) % 5][col_a]
            decrypted_text += table[(row_b - 1) % 5][col_b]
        else:
            decrypted_text += table[row_a][col_b]
            decrypted_text += table[row_b][col_a]
    
    return decrypted_text

def server_program():
    host = '127.0.0.1'
    port = 65432
    
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(2)
    conn, address = server_socket.accept()
    print(f"Connection from: {address}")
    
    key = "PLAYFAIR"
    
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        print(f"Received encrypted message: {data}")
        
        decrypted_message = playfair_decrypt(data, key)
        print(f"Decrypted message: {decrypted_message}")
    
    conn.close()

if __name__ == '__main__':
    server_program()