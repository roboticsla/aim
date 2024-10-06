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

def playfair_encrypt(text, key):
    text = text.upper().replace("J", "I")
    table = generate_playfair_table(key)
    encrypted_text = ""
    
    i = 0
    while i < len(text):
        a = text[i]
        if i + 1 < len(text):
            b = text[i + 1]
        else:
            b = 'X'
        
        if a == b:
            b = 'X'
            i += 1
        else:
            i += 2
        
        row_a, col_a = find_position(a, table)
        row_b, col_b = find_position(b, table)
        
        if row_a == row_b:
            encrypted_text += table[row_a][(col_a + 1) % 5]
            encrypted_text += table[row_b][(col_b + 1) % 5]
        elif col_a == col_b:
            encrypted_text += table[(row_a + 1) % 5][col_a]
            encrypted_text += table[(row_b + 1) % 5][col_b]
        else:
            encrypted_text += table[row_a][col_b]
            encrypted_text += table[row_b][col_a]
    
    return encrypted_text

def client_program():
    host = '127.0.0.1'
    port = 65432
    
    client_socket = socket.socket()
    client_socket.connect((host, port))
    
    key = "PLAYFAIR"
    
    message = input("Enter message to encrypt and send: ")
    encrypted_message = playfair_encrypt(message, key)
    
    client_socket.send(encrypted_message.encode())
    print(f"Sent encrypted message: {encrypted_message}")
    
    client_socket.close()

if __name__ == '__main__':
    client_program()