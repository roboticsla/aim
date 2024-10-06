import socket
import random

# Diffie-Hellman parameters (publicly agreed upon)
p = 23 
g = 5  

# private key for Agent 2
b = random.randint(1, p-1)
B = pow(g, b, p)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12346))
server_socket.listen(1)
conn, addr = server_socket.accept()

A = int(conn.recv(1024).decode())

conn.send(str(B).encode())

shared_secret = pow(A, b, p)
print(f"Shared Secret: {shared_secret}")

conn.close()
server_socket.close()
