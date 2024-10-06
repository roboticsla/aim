import socket

key = [1, 0, 1, 0, 0, 0, 0, 0, 1, 0]
P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
P8 = [6, 3, 7, 4, 8, 5, 10, 9]
IP = [2, 6, 3, 1, 4, 8, 5, 7]
EP = [4, 1, 2, 3, 2, 3, 4, 1]
P4 = [2, 4, 3, 1]
IP_inv = [4, 1, 3, 5, 7, 2, 8, 6]

S0 = [
    [1, 0, 3, 2],
    [3, 2, 1, 0],
    [0, 2, 1, 3],
    [3, 1, 3, 2]
]
S1 = [
    [0, 1, 2, 3],
    [2, 0, 1, 3],
    [3, 0, 1, 0],
    [2, 1, 0, 3]
]

key1 = [0] * 8
key2 = [0] * 8

def shift(ar, n):
    return ar[n:] + ar[:n]

def key_generation():
    global key1, key2

    key_ = [key[P10[i] - 1] for i in range(10)]

    Ls, Rs = key_[:5], key_[5:]
    Ls_1, Rs_1 = shift(Ls, 1), shift(Rs, 1)

    key_[:5], key_[5:] = Ls_1, Rs_1
    key1 = [key_[P8[i] - 1] for i in range(8)]

    Ls_2, Rs_2 = shift(Ls, 2), shift(Rs, 2)
    key_[:5], key_[5:] = Ls_2, Rs_2
    key2 = [key_[P8[i] - 1] for i in range(8)]

    print("Your Key-1 :")
    print(" ".join(map(str, key1)))

    print("Your Key-2 :")
    print(" ".join(map(str, key2)))

def binary_(val):
    return format(val, '02b')

def function_(ar, key_):
    l, r = ar[:4], ar[4:]

    ep = [r[EP[i] - 1] for i in range(8)]
    ep = [ep[i] ^ key_[i] for i in range(8)]

    l_1, r_1 = ep[:4], ep[4:]
    row, col = int(f'{l_1[0]}{l_1[3]}', 2), int(f'{l_1[1]}{l_1[2]}', 2)
    val = S0[row][col]
    str_l = binary_(val)

    row, col = int(f'{r_1[0]}{r_1[3]}', 2), int(f'{r_1[1]}{r_1[2]}', 2)
    val = S1[row][col]
    str_r = binary_(val)

    r_ = [int(str_l[i]) for i in range(2)] + [int(str_r[i]) for i in range(2)]
    r_p4 = [r_[P4[i] - 1] for i in range(4)]

    l = [l[i] ^ r_p4[i] for i in range(4)]
    return l + r

def swap(array, n):
    # Swap the nibbles of size n (4)
    return array[n:] + array[:n]

def decryption(ciphertext):
    arr = [ciphertext[IP[i] - 1] for i in range(8)]
    arr1 = function_(arr, key2)
    after_swap = swap(arr1, len(arr1) // 2)
    arr2 = function_(after_swap, key1)
    return [arr2[IP_inv[i] - 1] for i in range(8)]

def receive_from_client(data):
    received_array = list(map(int, data.split(" ")))
    decrypted = decryption(received_array)
    return " ".join(map(str, decrypted))

if __name__ == "__main__":
    key_generation() 
    host = '127.0.0.1'
    port = 65432

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(2)
    conn, address = server_socket.accept()

    key = [[4,3, 2],[3, 2, 1],[ 2, 1, 1]]

    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        print(f"Received encrypted message: {data}")
        
        decrypted_message = receive_from_client(data)
        print(f"Decrypted message: {decrypted_message}")

    conn.close()