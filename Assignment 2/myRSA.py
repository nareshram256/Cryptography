import numpy as np
import sympy as sy
import gmpy2
import random
import textwrap

# Key Generation
def gen_strong_prime(low):
    prime = random.randint(low, 2*low)
    count = 0
    # print("\nCount:")

    while True:
        count += 1
        # print(f"{count:3}", end=" | ")

        while True:
            rand_prime = sy.randprime(a=1, b=20)
            if sy.gcd(rand_prime, prime) == 1:
                break

        for t in range(10):
            if not gmpy2.is_strong_prp(prime, rand_prime):
                break
            return prime
            
        prime = sy.nextprime(prime)

def gen_keys(low):
    p, q = gen_strong_prime(low), gen_strong_prime(low)
    n = p*q
    phi_n = (p-1)*(q-1)
    while True:
        e = sy.randprime(a=1, b=20)
        if sy.gcd(e, phi_n) == 1:
            break
    d = sy.mod_inverse(e, phi_n)
    return n, e, d

# Processing
def str_to_blocks(msg:str, block_size:int):
    msg = "".join([str.zfill(str(ord(char) - 55), 2) for char in msg])
    blocks = textwrap.wrap(msg, block_size)
    return blocks

def blocks_to_str(blocks:list):
    for idx, block in enumerate(blocks):
        block = textwrap.wrap(block, 2)
        char = "".join([chr(int(num) + 55) for num in block])
        blocks[idx] = char
    return "".join(blocks)

# Encryption
def encrypt(blocks:list, key:tuple) -> list:
    n, e = key
    cip_blocks = [str(sy.Pow(int(block), e) % n) for block in blocks]

    return cip_blocks
