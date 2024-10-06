import socket
from sympy import mod_inverse

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

def simple_custom_hash(message):
    hash_value = 0
    prime = 31
    for char in message:
        hash_value = (hash_value * prime + ord(char)) % 2**16
    return hash_value

def receiver():
    sender_public_key, _ = rsa_keygen()
    receiver_public_key, receiver_private_key = rsa_keygen()
    s = socket.socket()
    s.bind(('localhost', 12345))
    s.listen(1)
    conn, addr = s.accept()
    encrypted_message = conn.recv(4096).decode()
    decrypted_message = rsa_decrypt(eval(encrypted_message), receiver_private_key)
    message, signature = decrypted_message.split("::")
    signature_list = list(map(int, signature.split(',')))
    message_hash = simple_custom_hash(message)
    decrypted_signature = ''.join(map(str, rsa_decrypt(signature_list, sender_public_key)))
    if str(message_hash) == decrypted_signature:
        print("Verification successful! Message is authentic.")
        print("Received message:", message)
    else:
        print("Verification failed! Message is not authentic.")

if __name__ == "__main__":
    receiver()
