import socket
from sympy import mod_inverse

# RSA key generation function (same as before)
def rsa_keygen():
    p = 61
    q = 53
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 17
    d = mod_inverse(e, phi)
    return (e, n), (d, n)

def rsa_encrypt(message, key):
    e, n = key
    return [pow(ord(char), e, n) for char in message]

def rsa_decrypt(ciphertext, key):
    d, n = key
    return ''.join([chr(pow(char, d, n)) for char in ciphertext])

# Simple custom hash function
def simple_custom_hash(message):
    hash_value = 0
    prime = 31
    for char in message:
        hash_value = (hash_value * prime + ord(char)) % 2**16
    return hash_value

def sender():
    sender_public_key, sender_private_key = rsa_keygen()
    receiver_public_key, _ = rsa_keygen()
    message = "Hello Secret Receiver"
    print("message = ", message)
    message_hash = simple_custom_hash(message)
    print("hashed message = ",message_hash)
    digital_signature = rsa_encrypt(str(message_hash), sender_private_key)
    digital_signature_str = ','.join(map(str, digital_signature))
    message_to_send = message + "::" + digital_signature_str
    encrypted_message = rsa_encrypt(message_to_send, receiver_public_key)
    s = socket.socket()
    s.connect(('localhost', 12345))
    s.sendall(str(encrypted_message).encode())
    s.close()

if __name__ == "__main__":
    sender()
