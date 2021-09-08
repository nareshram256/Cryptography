import numpy as np
import string
from sympy import Matrix
import sys

inputfile = sys.argv[1]
keyfile = sys.argv[2]
outputfile = sys.argv[3]

def get_key(key_file):
    with open(key_file, "r") as file:
        key = file.read()
        key = key.split(",")
        key = [int(s.strip()) for s in key]
        key_size = np.sqrt(len(key)).astype(int)

        #check key
        try:
            key = np.array(key).reshape(key_size, key_size)
        except ValueError:
            print("Incorrect keysize supplied!")
            print("Process terminated!")
            exit()
        
        if np.linalg.det(key) % 26 == 0:
            print("Singular key supplied!")
            print("Process terminated!")
            exit()

    return key, key_size

def invert_key(key):
    inv_key = Matrix(key).inv_mod(26)
    return np.array(inv_key)

def preprocess_cipher(inputfile, key_size):
    with open(inputfile, "r") as file:
        ciphertext = file.read()

    # replace characters by integers and return a list
    # string.ascii_lowercase.index() replaces alphabets by ints in range 0 to 25.
    processed_ciphertext = [string.ascii_lowercase.index(char) for char in ciphertext]

    # return reshaped numpy array
    return np.array(processed_ciphertext).reshape(-1, key_size)

def encrypt(processed_plaintext, key):
    # multiply modulo 26
    cipher = np.matmul(processed_plaintext, key) % 26

    # convert to list
    cipher = list(cipher.ravel())

    # relpace integers by characters
    cipher = [chr(num + 97) for num in cipher]

    # list to string
    cipher = str.join("", cipher)

    return cipher

def decrypt(ciphertext, inverted_key):
    return encrypt(ciphertext, inverted_key)

def write_to_disk(outstring, outputfile):
    with open(outputfile, "w") as file:
        file.write(outstring)

key, key_size = get_key(keyfile)
key = invert_key(key)
processed_ciphertext = preprocess_cipher(inputfile, key_size)
plaintext = decrypt(processed_ciphertext, key)
write_to_disk(plaintext, outputfile)