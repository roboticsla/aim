import numpy as np
import socket

def hillcipher_encrypt(msg, key):
    msg = msg.lower().replace(' ', '')
    msg += 'x'*(3-len(msg) % 3)
    msg = [ord(c) - ord('a') for c in msg]
    msg = np.array(msg).reshape(-1, 3)
    key = np.array(key).reshape(3, 3)
    encrypted_msg = np.matmul(msg, key) % 26
    return ''.join([chr(c + ord('a')) for c in encrypted_msg.flatten()])
 
 
if __name__ == '__main__':
    print("HILL CIPHER ENCRYPTION")
    host = '127.0.0.1'
    port = 65432
    
    client_socket = socket.socket()
    client_socket.connect((host, port))
    
    key = [[4,3, 2],[3, 2, 1],[ 2, 1, 1]]
    
    message = input("Enter message to encrypt and send: ")
    encrypted_message = hillcipher_encrypt(message, key)
    
    client_socket.send(encrypted_message.encode())
    print(f"Sent encrypted message: {encrypted_message}")
    
    client_socket.close()