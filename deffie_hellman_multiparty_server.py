import socket
import threading

# Common parameters (prime p and generator g)
p = 23  # Example prime
g = 5   # Example generator

# Function to handle client communication
def handle_client(client_socket, participant_id, public_keys, intermediate_secrets):
    try:
        # Step 1: Receive public key from the participant
        public_key = client_socket.recv(1024).decode()
        public_keys[participant_id] = int(public_key)
        print(f"Participant {participant_id} sent public key: {public_key}")
    except ValueError as e:
        print(f"Error receiving public key from participant {participant_id}: {e}")
        return
    
    # Wait until all public keys are received before sending them to the clients
    while None in public_keys:
        pass  # Keep waiting until all public keys are received

    # Step 2: Send the public keys to the client
    public_keys_str = "\n".join(str(key) for key in public_keys if key is not None)
    client_socket.sendall(public_keys_str.encode())

    # Step 3: Receive intermediate secret from client
    try:
        intermediate_secret = client_socket.recv(1024).decode()
        intermediate_secrets[participant_id] = int(intermediate_secret)
        print(f"Participant {participant_id} sent intermediate secret: {intermediate_secret}")
    except ValueError as e:
        print(f"Error receiving intermediate secret from participant {participant_id}: {e}")
        return

    # Wait until all intermediate secrets are received
    while None in intermediate_secrets:
        pass

    # Step 4: Send the next intermediate secret to the client
    intermediate_to_send = intermediate_secrets[(participant_id - 1) % 3]
    client_socket.send(str(intermediate_to_send).encode())

    client_socket.close()

def start_server():
    public_keys = [None, None, None]  # To hold public keys of A, B, and C
    intermediate_secrets = [None, None, None]  # To hold intermediate secrets
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 9999))
    server_socket.listen(3)
    print("Server listening on port 9999")

    while None in public_keys:  # Wait until all public keys are received
        client_socket, addr = server_socket.accept()
        participant_id = len([k for k in public_keys if k is not None])
        threading.Thread(target=handle_client, args=(client_socket, participant_id, public_keys, intermediate_secrets)).start()

if __name__ == "__main__":
    start_server()
