import numpy as np
import string
from sympy import Matrix

def remove(input_string):
    # bring input to lower case
    input_string = input_string.lower()

    # remove blank spaces
    input_string = input_string.replace(" ","")

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
    for char in input_string:
        # ord() returns ASCII value of the character supplied
        if ord(char) in special_chars:
            input_string = input_string.replace(char, "")

    return input_string

def preprocess_input(input_string, key_size):
    # remove symbols and spaces
    input_string = remove(input_string)

    # account for variable length
    if len(input_string) % key_size != 0:
        extra = key_size - (len(input_string) % key_size)
        input_string = input_string + extra * "x"

    # replace characters by integers and return a list
    # string.ascii_lowercase.index() replaces alphabets by ints in range 0 to 25.
    input_numbers_list = [string.ascii_lowercase.index(char) for char in input_string]

    # return reshaped numpy array
    return np.array(input_numbers_list).reshape(-1, key_size)

def encrypt(input_string, key):

    key_size = key.shape[0]

    # preprocess input_string
    input_array = preprocess_input(input_string, key_size)

    # multiply modulo 26
    cipher = np.matmul(input_array, key) % 26

    # convert to list
    cipher = list(cipher.ravel())

    # relpace integers by characters
    cipher = [chr(num + 97) for num in cipher]

    # list to string
    cipher = str.join("", cipher)

    return cipher

def invert_key(key):
    inv_key = Matrix(key).inv_mod(26)
    return np.array(inv_key)

def decrypt(input_string, inverted_key):
    return encrypt(input_string, inverted_key)