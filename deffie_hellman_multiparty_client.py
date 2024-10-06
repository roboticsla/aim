import socket
import random

# Common parameters (prime p and generator g)
p = 23  # Example prime
g = 5   # Example generator

def diffie_hellman_key_exchange(private_key, received_public_keys):
    # Calculate intermediate secrets for each public key received
    intermediate_secrets = [(pub_key ** private_key) % p for pub_key in received_public_keys]
    return intermediate_secrets

def calculate_final_shared_secret(intermediate_secret, private_key):
    # Final shared secret calculation
    return (intermediate_secret ** private_key) % p

def client(private_key, participant_id):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 9999))
    
    # Step 1: Compute and send public key
    public_key = (g ** private_key) % p
    client_socket.send(str(public_key).encode())
    print(f"Participant {participant_id} sent public key: {public_key}")
    
    # Step 2: Receive all public keys from the server
    received_public_keys = []
    try:
        data = client_socket.recv(1024).decode().strip()
        if data:
            received_public_keys = [int(key) for key in data.split("\n") if key]
            print(f"Participant {participant_id} received public keys: {received_public_keys}")
    except ValueError as e:
        print(f"Error receiving public keys: {e}")
        return  # Stop if there's an issue with public key reception
    
    # Remove own public key from the list
    if public_key in received_public_keys:
        received_public_keys.remove(public_key)

    # Step 3: Calculate intermediate secrets for each public key
    intermediate_secrets = diffie_hellman_key_exchange(private_key, received_public_keys)

    # Check if intermediate secrets list is populated correctly
    if len(intermediate_secrets) < 2:
        print(f"Error: insufficient intermediate secrets for participant {participant_id}")
        return

    # Step 4: Send intermediate secret to the next participant
    intermediate_secret_to_send = intermediate_secrets[(participant_id + 1) % len(intermediate_secrets)]
    client_socket.send(str(intermediate_secret_to_send).encode())
    print(f"Participant {participant_id} sent intermediate secret: {intermediate_secret_to_send}")
    
    # Step 5: Receive intermediate secret from the previous participant
    intermediate_secret_received = int(client_socket.recv(1024).decode().strip())
    print(f"Participant {participant_id} received intermediate secret: {intermediate_secret_received}")
    
    # Step 6: Calculate final shared secret
    shared_secret = calculate_final_shared_secret(intermediate_secret_received, private_key)
    print(f"Participant {participant_id}'s shared secret: {shared_secret}")
    
    client_socket.close()

if __name__ == "__main__":
    participant_id = int(input("Enter participant ID (0 for A, 1 for B, 2 for C): "))
    private_key = random.randint(1, 100)  # Generate a random private key for each client
    client(private_key, participant_id)
