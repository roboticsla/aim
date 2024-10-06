import socket
import random

# Diffie-Hellman parameters (publicly agreed upon)
p = 23 
g = 5   

# Generate private key for Agent 1
a = random.randint(1, p-1)
A = pow(g, a, p)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

client_socket.send(str(A).encode())

B = int(client_socket.recv(1024).decode())

shared_secret = pow(B, a, p)
print(f"Shared Secret: {shared_secret}")

client_socket.close()
