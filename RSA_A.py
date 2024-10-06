import socket
from sympy import mod_inverse

# RSA key generation for A (Sender)
p_A, q_A = 61, 53
n_A = p_A * q_A
phi_n_A = (p_A - 1) * (q_A - 1)
e_A = 17
d_A = mod_inverse(e_A, phi_n_A)
public_key_A = (e_A, n_A)
private_key_A = (d_A, n_A)

def sign_and_encrypt(message, private_key_A, public_key_B):
    signed_and_encrypted_message = ''
    for char in message:
        m = ord(char)
        signed_m = pow(m, private_key_A[0], private_key_A[1])
        encrypted_m = pow(signed_m, public_key_B[0], public_key_B[1])
        signed_and_encrypted_message += f'{encrypted_m} '
    return signed_and_encrypted_message.strip()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()
port = 12345

client_socket.connect((host, port))

# Receive B's public key
data = client_socket.recv(1024).decode()
e_B, n_B = map(int, data.split())
public_key_B = (e_B, n_B)

# Message to be sent
message = 'HELLOWORLDHOWAREYOU'

# Sign and encrypt the message
encrypted_message = sign_and_encrypt(message, private_key_A, public_key_B)

# Send the encrypted message and A's public key
client_socket.send(f"{encrypted_message};{public_key_A[0]};{public_key_A[1]}".encode())

client_socket.close()
