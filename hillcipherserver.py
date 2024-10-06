import numpy as np
import socket

def hillcipher_decrypt(encry, key):
    key_inv=np.linalg.inv(key)
    msg = [ord(c) - ord('a') for c in encry]
    msg = np.array(msg).reshape(-1, 3)
    decrypted_msg = np.matmul(msg, key_inv) % 26
    return ''.join([chr(int(c) + ord('a')) for c in decrypted_msg.flatten()])


host = '127.0.0.1'
port = 65432

server_socket = socket.socket()
server_socket.bind((host, port))
server_socket.listen(2)
conn, address = server_socket.accept()
print(f"Connection from: {address}")

key = [[4,3, 2],[3, 2, 1],[ 2, 1, 1]]

while True:
    data = conn.recv(1024).decode()
    if not data:
        break
    print(f"Received encrypted message: {data}")
    
    decrypted_message = hillcipher_decrypt(data, key)
    print(f"Decrypted message: {decrypted_message}")

conn.close()