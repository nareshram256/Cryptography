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
    for i in range(123, 127):
        special_chars.append(i)
    
    
    # remove special charcaters
    for char in plaintext:
        # ord() returns ASCII value of the character supplied
        if ord(char) in special_chars:
            plaintext = plaintext.replace(char, "")

    return plaintext

def preprocess_input(inputfile, key_size):
    with open(inputfile, "r") as file:
        plaintext = file.read()

    # remove symbols, spaces, and new lines
    plaintext = remove(plaintext)

    # account for variable length of plaintext
    if len(plaintext) % key_size != 0:
        extra = key_size - (len(plaintext) % key_size)
        plaintext = plaintext + extra * "x"

    # replace characters by integers and return a list
    # string.ascii_lowercase.index() replaces alphabets by ints in range 0 to 25.
    processed_plaintext = [string.ascii_lowercase.index(char) for char in plaintext]

    # return reshaped numpy array
    return np.array(processed_plaintext).reshape(-1, key_size)

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

def write_to_disk(outstring, outputfile):
    with open(outputfile, "w") as file:
        file.write(outstring)

key, key_size = get_key(keyfile)
processed_plaintext = preprocess_input(inputfile, key_size)
ciphertext = encrypt(processed_plaintext, key)
write_to_disk(ciphertext, outputfile)