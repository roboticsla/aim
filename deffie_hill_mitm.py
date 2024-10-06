import socket
import random

# Diffie-Hellman parameters (publicly agreed upon)
p = 23 
g = 5   

x = random.randint(1, p-1)
X = pow(g, x, p)

# MITM - Intercept and relay the messages
def mitm_attack():
    mitm_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mitm_socket.bind(('localhost', 12345))
    mitm_socket.listen(1)
    conn1, addr1 = mitm_socket.accept()

    mitm_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mitm_client_socket.connect(('localhost', 12346))

    # Intercept Agent 1's public key and send our public key to Agent 2
    A = int(conn1.recv(1024).decode())
    mitm_client_socket.send(str(X).encode())

    # Intercept Agent 2's public key and send our public key to Agent 1
    B = int(mitm_client_socket.recv(1024).decode())
    conn1.send(str(X).encode())

    # Compute the two shared secrets (one with Agent 1, one with Agent 2)
    shared_secret_with_agent1 = pow(A, x, p)
    shared_secret_with_agent2 = pow(B, x, p)

    print(f"Shared Secret with Agent 1: {shared_secret_with_agent1}")
    print(f"Shared Secret with Agent 2: {shared_secret_with_agent2}")

    conn1.close()
    mitm_client_socket.close()
    mitm_socket.close()

mitm_attack()
