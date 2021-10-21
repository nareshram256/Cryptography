import numpy as np
import sys
from sympy import Matrix

key_size = int(sys.argv[1])
outputfile = sys.argv[2]

def generate_key(key_size):
    key = np.random.randint(low=0, high=100, size=(key_size, key_size)) % 26
    return key

def invert_key(key):
    inv_key = Matrix(key).inv_mod(26) % 26
    return np.array(inv_key)

def mat_to_str(mat):
    mat_str = ",".join(list(map(str, mat.ravel())))
    return mat_str

i = 0
while True:
    key = generate_key(key_size)
    try:
        invert_key(key)
        break
    except ValueError:
        i += 1

print(key)
key_str = mat_to_str(key)

with open(outputfile, "w") as file:
    file.write(key_str)