import numpy as np
import re
# import sys

# inp_path = sys.argv[1] + '.txt'
# key_path = sys.argv[2] + '.txt'
# cipher_path = sys.argv[3] + '.txt'
# dec_path = sys.argv[4] + '.txt'

def process_inp(inp:str) -> str:
    '''
    args:
        inp: string. No restrictions on the string i.e. may have special characters, spaces, anything.
    returns:
        string containing only alphabets, all in uppercase with no spacces or newlines.
    '''
    return "".join(re.findall("[A-Z]+", inp.upper()))

def vig_encrypt(inp:str, key:str, dec:int=1) -> str:
    '''
    args:
        inp: str of the form returned by process_inp i.e. only alphabets, uppercase, no spaces
        key: str of the form returned by process_inp i.e. only alphabets, uppercase, no spaces
        dec: if set to 1, perform encryption. if set to -1, perform decryption

    returns:
        cipher: str of the form returned by process_inp i.e. only alphabets, uppercase, no spaces
    '''
    key_len = len(key)

    # account for variable length of plaintext
    if len(inp) % key_len != 0:
        extra = key_len - (len(inp) % key_len)
        inp = inp + extra * "x"

    cipher = np.zeros(shape = (len(inp),))
    inp_arr = np.array([ord(char) - 65 for char in inp])    # ord(A) == 65
    key_arr = dec * np.array([ord(char) - 65 for char in key])

    for i in range(0,len(inp), key_len):
        temp_inp_arr = inp_arr[i:i+key_len]
        cipher[i:i+key_len] = 65 + (temp_inp_arr + key_arr) % 26
    
    cipher = "".join([chr(int(num)) for num in cipher]).upper()
    return cipher

def vig_decrypt(cipher:str, key:str) -> str:
    '''
    args:
        inp: str of the form returned by process_inp i.e. only alphabets, uppercase, no spaces
        key: str of the form returned by process_inp i.e. only alphabets, uppercase, no spaces
    returns:
        cipher: str of the form returned by process_inp i.e. only alphabets, uppercase, no spaces
    '''
    return vig_encrypt(inp = cipher, key=key, dec=-1)

# with open(inp_path, "r") as i, open(key_path, "r") as k:
#     inp = i.read()
#     key = k.read()

# cipher = vig_encrypt(process_inp(inp), key)
# dec = vig_decrypt(cipher, key)

# with open(cipher_path, "w") as c, open(dec_path, "w") as d:
#     c.write(cipher)
#     d.write(dec)