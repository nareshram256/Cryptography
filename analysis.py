import sys
import numpy as np
from sympy import Matrix
from collections import Counter

ciphertext = sys.argv[1]
plaintext = sys.argv[2]
best_key_file_name = sys.argv[3]
    
def remove(plaintext):
    # bring input to lower case and remove new line characters.
    plaintext = plaintext.lower().replace("\n", "")

    # remove blank spaces
    plaintext = plaintext.replace(" ","")

    # ascii vallues of special characters: (32–47 / 58–64 / 91–96 / 123–126)
    special_chars = []
    for i in range(32, 58):
        special_chars.append(i)
    for i in range(58, 65):
        special_chars.append(i)
    for i in range(91, 97):
        special_chars.append(i)
    for i in range(126, 127):
        special_chars.append(i)
    
    # remove special charcaters
    for char in plaintext:
        # ord() returns ASCII value of the character supplied
        if ord(char) in special_chars:
            plaintext = plaintext.replace(char, "")

    return plaintext

def preprocess(text, key_size):
    # account for variable length of plaintext
    if len(text) % key_size != 0:
        extra = key_size - (len(text) % key_size)
        text = text + extra * "x"

    # replace characters by integers and return a list
    processed_plaintext = [ord(char) - 97 for char in text]

    # return reshaped numpy array
    return np.array(processed_plaintext).reshape(-1, key_size)

def invert_key(key):
    inv_key = Matrix(key).inv_mod(26) % 26
    return np.array(inv_key)

def find_inverted_key(known_cipher, known_plain):
    inv = np.array(Matrix(known_cipher).inv_mod(26))
    inverted_key = np.matmul(inv, known_plain)
    return inverted_key

def encrypt(processed_plaintext, key):
    # multiply modulo 26
    ciphertext = np.matmul(processed_plaintext, key) % 26

    # convert to list
    ciphertext = list(ciphertext.ravel())

    # relpace integers by characters
    ciphertext = [chr(num + 97) for num in ciphertext]

    # list to string
    ciphertext = str.join("", ciphertext)

    return ciphertext

def decrypt(ciphertext, inverted_key):
    return encrypt(ciphertext, inverted_key)

def index_of_coincidence(text):
    N = len(text)
    freq = Counter(text)
    freq = [val for val in freq.values()]
    IoC = sum([f*(f-1) for f in freq]) / (N * (N - 1))
    return IoC

def get_sub_sequences(seq, key_size):
    sub_sequences = []
    for i in range(key_size):
        sub_sequences.append(seq[i::key_size])
    return sub_sequences

def mat_to_str(mat):
    mat_str = ",".join(list(map(str, mat.ravel())))
    return mat_str

with open(ciphertext, "r") as c_file, open(plaintext, "r") as p_file:
    ciphertext = c_file.read()
    plaintext = p_file.read()

plaintext = remove(plaintext)
best = [0,0,0]

print("\n")
for key_size in range(2, 11):
    if key_size**2 > len(ciphertext):
        break
    print("\nkey_size:", key_size)

    start = 0
    while True:
        known_cipher = ciphertext[start:start+key_size**2]
        known_plain = plaintext[start:start+key_size**2]

        known_cipher = preprocess(known_cipher, key_size)
        known_plain = preprocess(known_plain, key_size)

        try:
            inverted_key = find_inverted_key(known_cipher, known_plain)
            key = invert_key(inverted_key)
            break
        except ValueError:
            start += 1
            if start > len(known_cipher) - key_size**2:
                break
    if start > len(known_cipher) - key_size**2:
        print("No invertible matrix for ciphertext found!")
        continue

    decrypted_text = decrypt(preprocess(ciphertext, key_size), inverted_key)
    IoC = index_of_coincidence(decrypted_text)
    print("IoC:", IoC)
    print("Key:")
    print(key)
    if best[1] < IoC:
        best = key_size, IoC, key

print("\n", 50*"#", "\n")
print("Best key_size:", best[0])
print("IoC:", best[1])
print("Key:\n", best[2])

with open(best_key_file_name, "w") as file:
    if best[0] == 0:
        file.write("No key found!")
    else:
        key_str = mat_to_str(best[2])
        file.write(key_str)